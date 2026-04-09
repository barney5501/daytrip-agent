import gradio as gr
import asyncio
from agent.agent import call_agent_async


async def prompt_agent(message, history):
    try:
        async for response, log in call_agent_async(message):
            yield response, log
    except Exception as e:
        yield (
            "סליחה, אני עמוס בפניות קודמות ולא יכול לענות כרגע. ניתן לנסות שוב בקרוב!",
            f"Error: {e}",
        )


with gr.Blocks(title="Travel Agent 📍") as demo:
    gr.Markdown("# Plan your day or activity and get tips and relevant information!")
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("מאחורי הקלעים")
            logs = gr.Code(label="שימוש בכלים", language="json")
        with gr.Column(scale=3):
            chat = gr.ChatInterface(
                fn=prompt_agent,
                examples=[
                    "מתי הכי טוב לרכב מחר על אופניים ברעננה?",
                    "כדאי לי לצאת לריצה מחר בבוקר במודיעין?",
                ],
                title="Chat",
                additional_outputs=[logs],
                cache_examples=False,
            )

if __name__ == "__main__":
    demo.launch()
