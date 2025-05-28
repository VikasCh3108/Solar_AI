# Shared utility functions for the project

def validate_rooftop_result(result):
    """
    Validate the Vision AI rooftop result structure and plausible values.
    Returns a tuple (is_valid, error_message)
    """
    if not result:
        return False, "No result returned."
    if not isinstance(result, dict):
        return False, "Result is not a dictionary."
    for field in ["mask", "usable_area_m2", "summary"]:
        if field not in result:
            return False, f"Missing field: {field}"
    if not isinstance(result["usable_area_m2"], (int, float)) or result["usable_area_m2"] <= 0:
        return False, "Usable area must be a positive number."
    if not isinstance(result["mask"], str) or len(result["mask"]) < 10:
        return False, "Mask format appears invalid."
    return True, "Valid rooftop result."

def compute_confidence_score(result):
    """
    Compute a confidence score for the Vision AI output.
    Returns the 'confidence' field if present and valid, else 0.95 as fallback.
    """
    if isinstance(result, dict) and "confidence" in result:
        try:
            conf = float(result["confidence"])
            if 0 <= conf <= 1:
                return conf
        except Exception:
            pass
    return 0.95
