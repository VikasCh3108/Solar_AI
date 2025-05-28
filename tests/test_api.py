import os
import io
import pytest
from fastapi.testclient import TestClient
from app import app
from PIL import Image

client = TestClient(app)

def create_test_image_bytes():
    img = Image.new('RGB', (512, 512), color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()

def test_analyze_endpoint_mock(monkeypatch):
    monkeypatch.setenv("MOCK_VISION_AI", "1")
    response = client.post("/analyze", files={"file": ("test.png", create_test_image_bytes(), "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert "rooftop" in data
    assert "assessment" in data
    assert "recommendation" in data
    assert "roi" in data
    assert data["rooftop"]["usable_area_m2"] > 0
    assert data["roi"]["cost_usd"] >= 0

def test_analyze_endpoint_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("MOCK_VISION_AI", "0")
    response = client.post("/analyze", files={"file": ("test.png", create_test_image_bytes(), "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert data["rooftop"]["usable_area_m2"] == 0.0
    assert "No rooftop area detected" in data["rooftop"]["summary"]
