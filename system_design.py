# Handles system design and recommendations

def recommend_system(context):
    """
    Suggest optimal panel type, number, and placement. Recommend inverter and mounting system.
    Args:
        context: Dict with all workflow data
    Returns:
        recommendation: Dict with system design
    """
    assessment = context.get('assessment', {})
    num_panels = assessment.get('layout_options', [{}])[0].get('panel_count', 0)
    recommendation = {
        "panel_type": "Monocrystalline 400W",
        "num_panels": num_panels,
        "layout": [{"x": 10, "y": 20, "width": 1, "height": 2}],
        "inverter": "5kW string inverter",
        "mounting": "flush mount"
    }
    return recommendation
