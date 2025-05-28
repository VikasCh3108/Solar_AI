# Handles rooftop detection and segmentation using Vision AI (e.g., OpenAI GPT-4 Vision)
import openai
import io
import os
from dotenv import load_dotenv

import json
import re
import base64

def detect_and_segment_rooftop(image):
    """
    Use Vision AI model to detect rooftop boundaries and segment usable area.
    Args:
        image: Preprocessed PIL.Image object
    Returns:
        rooftop_mask: Dict with fields mask, usable_area_m2, summary
    """
    load_dotenv()
    # Mock mode for simulation
    if os.environ.get("MOCK_VISION_AI") == "1":
        import random
        print("[MOCK] Returning simulated Vision AI output.")
        mock_result = {
            "mask": "POLYGON((100,100),(400,100),(400,400),(100,400))",
            "usable_area_m2": 42.3,
            "summary": "Rooftop area detected and segmented. Usable area is approximately 42.3 m^2.",
            "confidence": round(random.uniform(0.7, 0.99), 2)
        }
        print(f"Parsed Vision AI JSON: {mock_result}")
        return mock_result

    api_key = os.environ.get("OPENAI_API_KEY")  # Loaded from .env
    if not api_key:
        print("OPENAI_API_KEY not set in environment or .env file.")
        return None
    openai.api_key = api_key

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    print("Sending image to Vision AI API for rooftop detection...")
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Updated to gpt-4o, OpenAI's latest multimodal model (May 2025)

            messages=[
                {"role": "system", "content": (
                    "You are a solar analysis assistant. "
                    "Given a rooftop image, always return ONLY a strict JSON object (no explanation, no markdown, no extra text) with these fields: "
                    "mask (as a description or coordinates), usable_area_m2 (float), summary (string), confidence (float between 0 and 1). "
                    "Example: {\"mask\": \"polygon coordinates...\", \"usable_area_m2\": 40.5, \"summary\": \"Rooftop area detected...\", \"confidence\": 0.92}"
                )},
                {"role": "user", "content": [
                    {"type": "text", "text": (
                        "Identify the rooftop boundaries and usable area in this image. "
                        "Return ONLY a strict JSON object with: mask (as a description or coordinates), usable_area_m2 (float), summary (string), and confidence (float between 0 and 1)."
                    )},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(img_bytes.getvalue()).decode()}}
                ]}
            ],
            max_tokens=1024
        )
        content = response.choices[0].message.content
        if content is None:
            print("[ERROR] Vision AI API did not return any content. Raw response:")
            print(response)
            return None
        ai_content = content.strip()
        print(f"Vision AI raw response: {ai_content}")

        # Extract JSON from response (handle code blocks or extra text)
        json_str = ai_content
        # Remove markdown code block if present
        if json_str.startswith('```json'):
            json_str = re.sub(r'^```json|```$', '', json_str).strip()
        elif json_str.startswith('```'):
            json_str = re.sub(r'^```|```$', '', json_str).strip()
        # Find the first JSON object in the string
        match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if match:
            json_str = match.group(0)
        try:
            result = json.loads(json_str)
            # Validate required fields
            for field in ["mask", "usable_area_m2", "summary", "confidence"]:
                if field not in result:
                    raise ValueError(f"Missing field: {field}")
            # Ensure confidence is a float
            result["confidence"] = float(result["confidence"])
            print(f"Parsed Vision AI JSON: {result}")
            return result
        except Exception as e:
            print(f"Error parsing Vision AI JSON: {e}\nRaw response: {ai_content}")
            return None
    except Exception as e:
        print(f"Vision AI API error: {e}")
        return None
