# Solar Vision AI Rooftop Analysis Tool

## Project Overview
This project is an AI-powered rooftop solar analysis tool that allows users to upload rooftop images and receive a detailed, structured report on solar potential, system design, and ROI analysis. It features a FastAPI backend (with OpenAI Vision AI integration) and a Gradio-based Python frontend.

---

## 1. Project Setup Instructions

### Prerequisites
- Python 3.8+

### Backend Setup
1. Clone the repository and navigate to the backend directory.
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-...
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

## Quickstart

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the backend API:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
3. In a new terminal, launch the Gradio UI:
   ```bash
   python3 demo_gradio.py
   ```
4. Open the local Gradio URL (e.g., http://127.0.0.1:7860) in your browser.

---

### Frontend (Gradio)
- **demo_gradio.py**: Minimal Gradio app for uploading rooftop images and viewing analysis results. 

---

## 2. Implementation Documentation

### Backend (Python/FastAPI)
- **app.py**: Main FastAPI app, exposes `/analyze` endpoint for image analysis.
- **rooftop_detection.py**: Integrates with OpenAI Vision AI for rooftop segmentation and analysis.
- **utils.py**: Validation and confidence scoring utilities.
- **solar_assessment.py, system_design.py, cost_roi_analysis.py**: Solar potential, system design, and ROI logic.
- **tests/**: Automated unit and integration tests (run with `pytest`).

### Frontend (Gradio)
- **demo_gradio.py**: Minimal Gradio app for uploading rooftop images and viewing analysis results.

### Data Flow
1. User uploads rooftop image (frontend).
2. Image sent to `/analyze` endpoint (backend).
3. Backend processes image, runs Vision AI, validates results, computes confidence, performs assessment/design/ROI.
4. Structured JSON response returned to frontend for display.

---

## 3. Example Use Cases

- **Homeowner**: Uploads a photo of their rooftop to estimate solar potential and get a custom system/ROI report.
- **Solar Professional**: Uses the tool for quick site assessment and to generate client-ready reports.
- **Educational**: Demonstrates AI-powered computer vision for renewable energy applications.

---

---

## 4. Example Usage

- Upload a rooftop image via the web interface or use the API directly:
  ```bash
  curl -X POST -F "file=@examples/sample_input_image.png" http://localhost:8000/analyze
  ```
- Example request and output can be found in the `examples/` directory:
  - `examples/results___7_0.png` (input)
  - `examples/sample_api_request.json` (API call)
  - `examples/sample_output_response.json` (expected output)

---

## 5. Future Improvement Suggestions

- **Advanced Mask Visualization**: Overlay detected rooftop mask on the image in the frontend.
- **Real Weather API Integration**: Replace mock weather data with live API calls.
- **Enhanced Error Handling**: User-friendly error messages and frontend feedback.
- **User Authentication**: Enable user accounts and save analysis history.
- **Scalability**: Deploy on cloud infrastructure for public access.
- **More Test Coverage**: Add tests for all endpoints and edge cases.
- **Accessibility & UX**: Improve UI for accessibility and mobile responsiveness.
- **Report Export**: Generate downloadable PDF/HTML reports for users.

---

For any questions or contributions, please open an issue or pull request!
