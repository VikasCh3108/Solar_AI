import gradio as gr
import requests
from PIL import Image
import io
import json

def analyze_image_gradio(image):
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    files = {'file': ('upload.png', buf, 'image/png')}
    try:
        response = requests.post('http://localhost:8000/analyze', files=files)
        if response.status_code == 200:
            result = response.json()
            rooftop = result.get('rooftop', {})
            validation = result.get('rooftop_validation', {})
            assessment = result.get('assessment', {})
            recommendation = result.get('recommendation', {})
            roi = result.get('roi', {})
            summary = rooftop.get('summary', 'No summary')
            conf = rooftop.get('confidence', 'N/A')
            valid_conf = validation.get('confidence', 'N/A')
            validation_msg = validation.get('validation_msg', 'N/A')
            assessment_str = json.dumps(assessment, indent=2)
            recommendation_str = json.dumps(recommendation, indent=2)
            roi_str = json.dumps(roi, indent=2)
            pretty_json = json.dumps(result, indent=2)
            return (
                summary,
                conf,
                valid_conf,
                validation_msg,
                assessment_str,
                recommendation_str,
                roi_str,
                pretty_json,
                image
            )
        else:
            return ("Error: " + response.text,) + ("",) * 7 + (image,)
    except Exception as e:
        return (f"Exception: {e}",) + ("",) * 7 + (image,)

with gr.Blocks(title="Solar Rooftop Analysis Demo") as demo:
    gr.Markdown("""
    # Solar Rooftop Analysis Demo
    Upload a rooftop image to get AI-powered analysis and dynamic confidence scores. Backend must be running on localhost:8000.
    """)
    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="Upload Rooftop Image")
            submit_btn = gr.Button("Analyze")
        with gr.Column():
            gr.Markdown("## Analysis Summary")
            summary_out = gr.Textbox(label="Summary", interactive=False)
            conf_out = gr.Textbox(label="Vision AI Confidence", interactive=False)
            valid_conf_out = gr.Textbox(label="Validated Confidence", interactive=False)
            validation_msg_out = gr.Textbox(label="Validation Message", interactive=False)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Assessment")
            assessment_out = gr.Textbox(label="Assessment", lines=4, interactive=False)
        with gr.Column():
            gr.Markdown("### Recommendation")
            recommendation_out = gr.Textbox(label="Recommendation", lines=4, interactive=False)
        with gr.Column():
            gr.Markdown("### ROI / Cost Analysis")
            roi_out = gr.Textbox(label="ROI / Cost Analysis", lines=4, interactive=False)
    with gr.Row():
        gr.Markdown("### Input Image")
        img_out = gr.Image(label="Input Image", interactive=False)
    with gr.Accordion("Full API JSON Response", open=False):
        json_out = gr.Textbox(label="Full API JSON", lines=16, show_copy_button=True, interactive=False)
    submit_btn.click(
        analyze_image_gradio,
        inputs=img_input,
        outputs=[summary_out, conf_out, valid_conf_out, validation_msg_out, assessment_out, recommendation_out, roi_out, json_out, img_out],
        api_name="analyze_image_gradio"
    )

if __name__ == "__main__":
    demo.launch()
