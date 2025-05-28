from solar_assessment import assess_solar_potential
import pytest

def test_assess_solar_potential_basic():
    context = {
        "rooftop": {"usable_area_m2": 40},
        "weather": {"average_irradiance_kwh_m2_year": 1700}
    }
    assessment = assess_solar_potential(context)
    assert assessment["usable_area_m2"] == 40
    assert assessment["estimated_irradiation_kwh_per_m2_year"] == 1700
    assert isinstance(assessment["layout_options"], list)
    assert assessment["layout_options"][0]["panel_count"] == 20

def test_assess_solar_potential_zero_area():
    context = {
        "rooftop": {"usable_area_m2": 0},
        "weather": {"average_irradiance_kwh_m2_year": 1500}
    }
    assessment = assess_solar_potential(context)
    assert assessment["usable_area_m2"] == 0
    assert assessment["estimated_irradiation_kwh_per_m2_year"] == 1500
    assert assessment["layout_options"][0]["panel_count"] == 0
