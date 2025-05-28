import os
import pytest
from PIL import Image
from rooftop_detection import detect_and_segment_rooftop
from utils import validate_rooftop_result, compute_confidence_score

@pytest.fixture
def test_image(tmp_path):
    # Create a simple blank image for testing
    img_path = tmp_path / "test.png"
    img = Image.new('RGB', (512, 512), color='white')
    img.save(img_path)
    return Image.open(img_path)

def test_detect_and_segment_rooftop_mock(monkeypatch, test_image):
    # Force mock mode
    monkeypatch.setenv("MOCK_VISION_AI", "1")
    result = detect_and_segment_rooftop(test_image)
    assert isinstance(result, dict)
    assert "mask" in result and "usable_area_m2" in result and "summary" in result
    assert result["usable_area_m2"] > 0
    assert isinstance(result["mask"], str)
    is_valid, msg = validate_rooftop_result(result)
    assert is_valid, f"Validation failed: {msg}"
    confidence = compute_confidence_score(result)
    assert 0 <= confidence <= 1

def test_detect_and_segment_rooftop_no_api_key(monkeypatch, test_image):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_VISION_AI", "0")
    # Accept either None or fallback dict as valid result
    result = detect_and_segment_rooftop(test_image)
    if result is None:
        assert result is None
    else:
        # Accept fallback dict with any string mask and 0 usable_area_m2 as valid
        assert isinstance(result, dict)
        assert isinstance(result.get("mask"), str)
        assert result.get("usable_area_m2") == 0.0
        assert "No rooftop area detected" in result.get("summary", "")

def test_validate_rooftop_result_invalid():
    # Missing fields
    invalid = {"mask": "", "usable_area_m2": -1}
    is_valid, msg = validate_rooftop_result(invalid)
    assert not is_valid
    # Wrong type
    is_valid, msg = validate_rooftop_result("not a dict")
    assert not is_valid
    # Empty result
    is_valid, msg = validate_rooftop_result(None)
    assert not is_valid

def test_compute_confidence_score():
    result = {"mask": "POLYGON((100,100),(400,100),(400,400),(100,400))", "usable_area_m2": 42.3, "summary": "test"}
    score = compute_confidence_score(result)
    assert 0 <= score <= 1
