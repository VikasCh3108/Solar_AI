# Handles cost and ROI analysis

def analyze_cost_and_roi(context):
    """
    Estimate installation cost, incentives, payback period, ROI, and savings using context.
    Args:
        context: Dict with all workflow data
    Returns:
        roi_report: Dict with cost and ROI estimates
    """
    recommendation = context.get('recommendation', {})
    num_panels = recommendation.get('num_panels', 0)
    cost = num_panels * 500  # Example: $500 per panel
    roi_report = {
        "cost_usd": cost,
        "estimated_annual_savings_usd": 1600,
        "roi_percent": 17.8,
        "payback_period_years": 5.6,
        "incentives_usd": 2000
    }
    return roi_report
