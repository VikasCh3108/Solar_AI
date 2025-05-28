from system_design import recommend_system
import pytest

def test_recommend_system_basic():
    context = {"assessment": {"layout_options": [{"panel_count": 12}]}}
    rec = recommend_system(context)
    assert rec["panel_type"] == "Monocrystalline 400W"
    assert rec["num_panels"] == 12
    assert isinstance(rec["layout"], list)
    assert rec["inverter"] == "5kW string inverter"
    assert rec["mounting"] == "flush mount"

def test_recommend_system_zero_panels():
    context = {"assessment": {"layout_options": [{"panel_count": 0}]}}
    rec = recommend_system(context)
    assert rec["num_panels"] == 0
