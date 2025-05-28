# Handles solar potential assessment

def assess_solar_potential(context):
    """
    Calculate usable area, estimate irradiation, assess panel layout options using context (multi-source).
    Args:
        context: Dict with all workflow data (user input, rooftop, weather, shading, etc.)
    Returns:
        assessment: Dict with solar potential metrics
    """
    rooftop = context.get('rooftop', {})
    weather = context.get('weather', {})
    usable_area = rooftop.get('usable_area_m2', 0)
    irradiation = weather.get('average_irradiance_kwh_m2_year', 0)
    assessment = {
        "usable_area_m2": usable_area,
        "estimated_irradiation_kwh_per_m2_year": irradiation,
        "layout_options": [
            {"panel_count": int(usable_area // 2.0), "orientation": "south", "tilt": 20}
        ]
    }
    return assessment
