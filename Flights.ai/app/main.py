import gradio as gr
from .chat import chat
from .voice import text_to_speech

def chat_fn(message, history):
    history, reply, _ = chat(message, history)
    audio_path = text_to_speech(reply)
    return history, audio_path

with gr.Blocks() as ui:
    gr.Markdown("# ✈️ FlightAI — Local Airline Assistant (Phi-3 + Amadeus)")
    with gr.Row():
        chatbot = gr.Chatbot(label="FlightAI Chat", height=500, type="messages")
    with gr.Row():
        audio_output = gr.Audio(label="Voice Response", autoplay=True)
    with gr.Row():
        msg = gr.Textbox(label="Ask FlightAI anything about flights, prices, etc.")

    msg.submit(chat_fn, inputs=[msg, chatbot], outputs=[chatbot, audio_output])

ui.launch(inbrowser=True)