from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from PIL import Image
import io
import os
import time
import logging
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from image_acquisition import fetch_and_preprocess_image
from rooftop_detection import detect_and_segment_rooftop
from shading_analysis import analyze_shading_and_obstacles
from solar_assessment import assess_solar_potential
from system_design import recommend_system
from cost_roi_analysis import analyze_cost_and_roi
from report_generation import generate_report
from utils import validate_rooftop_result, compute_confidence_score

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("performance")

# Prometheus metrics
ANALYZE_REQUESTS = Counter('analyze_requests_total', 'Total /analyze requests')
ANALYZE_LATENCY = Histogram('analyze_latency_seconds', 'Latency for /analyze endpoint (seconds)')
ROOFTOP_LATENCY = Histogram('rooftop_detection_latency_seconds', 'Latency for rooftop detection (seconds)')
VALIDATION_LATENCY = Histogram('validation_latency_seconds', 'Latency for validation (seconds)')
SHADING_LATENCY = Histogram('shading_analysis_latency_seconds', 'Latency for shading analysis (seconds)')
ASSESSMENT_LATENCY = Histogram('assessment_latency_seconds', 'Latency for solar assessment (seconds)')
RECOMMENDATION_LATENCY = Histogram('recommendation_latency_seconds', 'Latency for system recommendation (seconds)')
ROI_LATENCY = Histogram('roi_latency_seconds', 'Latency for ROI analysis (seconds)')

app = FastAPI()

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # Increment Prometheus request counter
    ANALYZE_REQUESTS.inc()
    perf = {}
    start_time = time.time()

    # Read image from upload and preprocess
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    image = image.resize((512, 512))

    # Initialize context for analysis results and tracking
    context = {}
    context['user_input'] = {"image_file": file.filename}
    context['image'] = image

    # Insert mock weather data (replace with real API for production)
    context['weather'] = {
        "average_irradiance_kwh_m2_year": 1700,
        "climate_zone": "Temperate",
        "sunny_days_per_year": 220
    }

    # --- Rooftop Detection ---
    t0 = time.time()
    with ROOFTOP_LATENCY.time():
        rooftop_result = detect_and_segment_rooftop(image)
    perf['rooftop_detection_sec'] = time.time() - t0
    print(f"[PERF] Rooftop detection: {perf['rooftop_detection_sec']:.3f}s")
    logger.info(f"Rooftop detection: {perf['rooftop_detection_sec']:.3f}s")
    # Defensive: handle None or bad output from detection
    if not rooftop_result or not isinstance(rooftop_result, dict):
        error_result = {
            "mask": None,
            "usable_area_m2": None,
            "summary": "Rooftop detection failed.",
            "confidence": 0.0
        }
        context['rooftop'] = error_result
        context['rooftop_validation'] = {
            'is_valid': False,
            'validation_msg': 'Rooftop detection failed.',
            'confidence': 0.0
        }
        # Remove raw image from response
        context_to_return = {k: v for k, v in context.items() if k != 'image'}
        return JSONResponse(content=context_to_return, status_code=400)
    # Always propagate the confidence value to the rooftop result for the API response
    confidence = rooftop_result.get('confidence', 0.0)
    rooftop_result['confidence'] = confidence
    context['rooftop'] = rooftop_result

    # --- Rooftop Validation ---
    t0 = time.time()
    with VALIDATION_LATENCY.time():
        is_valid, validation_msg = validate_rooftop_result(rooftop_result)
        confidence = compute_confidence_score(rooftop_result) if is_valid else 0.0
    perf['validation_sec'] = time.time() - t0
    print(f"[PERF] Validation: {perf['validation_sec']:.3f}s")
    logger.info(f"Validation: {perf['validation_sec']:.3f}s")
    context['rooftop_validation'] = {
        'is_valid': is_valid,
        'validation_msg': validation_msg,
        'confidence': confidence
    }

    # --- Shading Analysis ---
    t0 = time.time()
    with SHADING_LATENCY.time():
        shading_map = analyze_shading_and_obstacles(image, rooftop_result)
    perf['shading_analysis_sec'] = time.time() - t0
    print(f"[PERF] Shading analysis: {perf['shading_analysis_sec']:.3f}s")
    logger.info(f"Shading analysis: {perf['shading_analysis_sec']:.3f}s")
    context['shading'] = shading_map

    # --- Solar Assessment ---
    t0 = time.time()
    with ASSESSMENT_LATENCY.time():
        assessment = assess_solar_potential(context)
    perf['solar_assessment_sec'] = time.time() - t0
    print(f"[PERF] Solar assessment: {perf['solar_assessment_sec']:.3f}s")
    logger.info(f"Solar assessment: {perf['solar_assessment_sec']:.3f}s")
    context['assessment'] = assessment

    # --- System Recommendation ---
    t0 = time.time()
    with RECOMMENDATION_LATENCY.time():
        recommendation = recommend_system(context)
    perf['recommendation_sec'] = time.time() - t0
    print(f"[PERF] System recommendation: {perf['recommendation_sec']:.3f}s")
    logger.info(f"System recommendation: {perf['recommendation_sec']:.3f}s")
    context['recommendation'] = recommendation

    # --- ROI Analysis ---
    t0 = time.time()
    with ROI_LATENCY.time():
        roi_report = analyze_cost_and_roi(context)
    perf['roi_analysis_sec'] = time.time() - t0
    print(f"[PERF] ROI analysis: {perf['roi_analysis_sec']:.3f}s")
    logger.info(f"ROI analysis: {perf['roi_analysis_sec']:.3f}s")
    context['roi'] = roi_report

    # Report path (placeholder, not an actual file)
    context['report_path'] = "report.pdf"

    # --- Performance Metrics ---
    duration = time.time() - start_time
    logger.info(f"/analyze processed in {duration:.3f} seconds for file {file.filename}")
    print(f"[PERF] /analyze processed in {duration:.3f} seconds for file {file.filename}")
    ANALYZE_LATENCY.observe(duration)
    perf['total_analysis_sec'] = duration
    context['performance'] = perf

    # Return all context except the raw image object (for serialization safety)
    context_to_return = {k: v for k, v in context.items() if k != 'image'}
    return JSONResponse(content=context_to_return)
