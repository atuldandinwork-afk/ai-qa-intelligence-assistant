import gradio as gr

from src.rag.unified_handler import handle_query
from src.ui.plotters import render_execution_trend
from src.ui.plotters import (
    render_execution_trend,
    render_automation_coverage,
    render_defect_distribution,
)



def gradio_handler(user_query):
    """
    Single entry point for Gradio UI.
    """
    result = handle_query(user_query)
 
    if result is None:
        return "I don't know.", None
    fig = None
    if result.get("visual"):
        if result["visual_type"] == "execution_trend":
            fig = render_execution_trend(result["visual_payload"])
        elif result["visual_type"] == "automation_coverage":
            fig = render_automation_coverage(result["visual_payload"])
        elif result["visual_type"] == "defect_distribution":
            fig = render_defect_distribution(result["visual_payload"])

    return result.get("text", ""), fig


with gr.Blocks(title="AI QA Intelligence Assistant") as demo:
    gr.Markdown("## 🧠 AI QA Intelligence Assistant")
    gr.Markdown(
        "Ask questions about test automation, execution, defects, and trends.\n"
        "Charts appear automatically when applicable."
    )

    with gr.Row():
        with gr.Column(scale=3):
            user_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g. Show execution trend",
            )
            submit_btn = gr.Button("Ask")

        with gr.Column(scale=5):
            answer_output = gr.Textbox(
                label="Answer",
                lines=6,
            )
            chart_output = gr.Plot(label="Visualization")

    submit_btn.click(
        fn=gradio_handler,
        inputs=user_input,
        outputs=[answer_output, chart_output],
    )


if __name__ == "__main__":
    demo.launch()
