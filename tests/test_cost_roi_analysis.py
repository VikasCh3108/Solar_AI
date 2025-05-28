from cost_roi_analysis import analyze_cost_and_roi
import pytest

def test_analyze_cost_and_roi_basic():
    context = {"recommendation": {"num_panels": 10}}
    roi = analyze_cost_and_roi(context)
    assert roi["cost_usd"] == 5000
    assert roi["estimated_annual_savings_usd"] == 1600
    assert roi["roi_percent"] == 17.8
    assert roi["payback_period_years"] == 5.6
    assert roi["incentives_usd"] == 2000

def test_analyze_cost_and_roi_zero_panels():
    context = {"recommendation": {"num_panels": 0}}
    roi = analyze_cost_and_roi(context)
    assert roi["cost_usd"] == 0
