# Handles image acquisition and preprocessing

import requests
from PIL import Image
from io import BytesIO
import os

def fetch_and_preprocess_image(user_input):
    """
    Fetch satellite image based on address using a public API, or load a local image file.
    Apply preprocessing (resize, normalize, enhance, etc).
    Args:
        user_input (dict): Contains address, image file, user type, etc.
    Returns:
        image: Preprocessed image object (PIL.Image)
    """
    address = user_input.get("address")
    image_file = user_input.get("image_file")
    image = None

    if image_file:
        if os.path.exists(image_file):
            image = Image.open(image_file)
            print(f"Loaded local image: {image_file}")
        else:
            print(f"Image file not found: {image_file}")
            return None
    elif address:
        # Example using Mapbox Static API (user must supply API key)
        API_KEY = "YOUR_MAPBOX_API_KEY"  # <-- Replace with your real API key
        url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{address}/auto/512x512?access_token={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            print(f"Fetched satellite image for address: {address}")
        except Exception as e:
            print(f"Error fetching satellite image: {e}")
            return None
    else:
        print("No address or image file provided.")
        return None

    # Example preprocessing: resize, convert to RGB
    image = image.convert('RGB').resize((512, 512))
    return image
