from utils import validate_rooftop_result, compute_confidence_score
import pytest

def test_validate_rooftop_result_valid():
    valid = {"mask": "polygon coordinates...", "usable_area_m2": 10.5, "summary": "ok"}
    is_valid, msg = validate_rooftop_result(valid)
    assert is_valid
    assert msg == "Valid rooftop result."

def test_validate_rooftop_result_invalid_cases():
    # Missing fields
    invalid = {"mask": "", "usable_area_m2": -1}
    is_valid, msg = validate_rooftop_result(invalid)
    assert not is_valid
    # Not a dict
    is_valid, msg = validate_rooftop_result("not a dict")
    assert not is_valid
    # Empty result
    is_valid, msg = validate_rooftop_result(None)
    assert not is_valid

def test_compute_confidence_score():
    result = {"mask": "polygon coordinates...", "usable_area_m2": 42.3, "summary": "test"}
    score = compute_confidence_score(result)
    assert 0 <= score <= 1
