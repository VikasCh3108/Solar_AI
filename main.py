# Entry point for the AI-powered rooftop analysis workflow
from image_acquisition import fetch_and_preprocess_image
from rooftop_detection import detect_and_segment_rooftop
from shading_analysis import analyze_shading_and_obstacles
from solar_assessment import assess_solar_potential
from system_design import recommend_system
from cost_roi_analysis import analyze_cost_and_roi
from report_generation import generate_report
from user_feedback import collect_user_feedback
from utils import validate_rooftop_result, compute_confidence_score

import argparse
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def fetch_mock_weather(address):
    # Simulate fetching weather/irradiance data for a given address
    return {
        "average_irradiance_kwh_m2_year": 1700,
        "climate_zone": "Temperate",
        "sunny_days_per_year": 220
    }

import time
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("performance")
    start_time = time.time()

    parser = argparse.ArgumentParser(description="AI Rooftop Solar Analysis")
    parser.add_argument('--address', type=str, help='Address to analyze (for satellite image fetch)')
    parser.add_argument('--image', type=str, help='Path to local rooftop image (optional)')
    parser.add_argument('--user_type', type=str, default='homeowner', help='User type: homeowner or professional')
    args = parser.parse_args()

    context = {}
    context['user_input'] = {
        "address": args.address,
        "image_file": args.image,
        "user_type": args.user_type
    }

    # Multi-source: Add mock weather data
    if args.address:
        context['weather'] = fetch_mock_weather(args.address)
    else:
        context['weather'] = fetch_mock_weather('default')

    print("1. Image Acquisition & Preprocessing...")
    image = fetch_and_preprocess_image(context['user_input'])
    context['image'] = image

    print("2. Rooftop Detection & Segmentation...")
    rooftop_result = detect_and_segment_rooftop(image)
    context['rooftop'] = rooftop_result

    # Validate and score Vision AI output
    is_valid, validation_msg = validate_rooftop_result(rooftop_result)
    confidence = compute_confidence_score(rooftop_result) if is_valid else 0.0
    context['rooftop_validation'] = {
        'is_valid': is_valid,
        'validation_msg': validation_msg,
        'confidence': confidence
    }

    print("\nStructured Vision AI Output:")
    if rooftop_result:
        print(f"Mask: {rooftop_result['mask']}")
        print(f"Usable Area (m^2): {rooftop_result['usable_area_m2']}")
        print(f"Summary: {rooftop_result['summary']}")
        print(f"Validation: {validation_msg}")
        print(f"Confidence Score: {confidence:.2f}")
        if not is_valid:
            print("[WARNING] Rooftop output failed validation. Downstream results may be unreliable.")
        elif confidence < 0.7:
            print("[WARNING] Confidence score is low. Please verify the result.")
    else:
        print("Vision AI did not return a valid result.")
        return

    print("3. Shading & Obstacle Analysis...")
    shading_map = analyze_shading_and_obstacles(image, rooftop_result)
    context['shading'] = shading_map

    print("4. Solar Potential Assessment...")
    assessment = assess_solar_potential(context)
    context['assessment'] = assessment

    print("5. System Design & Recommendation...")
    recommendation = recommend_system(context)
    context['recommendation'] = recommendation

    print("6. Cost & ROI Analysis...")
    roi_report = analyze_cost_and_roi(context)
    context['roi'] = roi_report

    print("7. Report Generation...")
    report_path = generate_report(context)
    print(f"Report generated at: {report_path}")
    context['report_path'] = report_path

    print("8. User Feedback & Iteration...")
    feedback = collect_user_feedback(report_path)
    context['feedback'] = feedback
    print(f"Feedback: {feedback}")

    # Performance metrics
    duration = time.time() - start_time
    logger.info(f"Main workflow completed in {duration:.3f} seconds")
    print(f"[PERF] Main workflow completed in {duration:.3f} seconds")
    context['performance'] = {"workflow_time_sec": duration}

if __name__ == "__main__":
    main()
