import gradio as gr
import asyncio
from agent.agent import call_agent_async


def agent_response_handler():
    pass


def prompt_agent(message, history):
    try:
        response = asyncio.run(call_agent_async(message))
        return response["AgentResponse"]
    except Exception as e:
        print("Exception", e)
        return (
            "סליחה, אני עמוס בפניות קודמות ולא יכול לענות כרגע. ניתן לנסות שוב בקרוב!"
        )


with gr.Blocks(title="Travel Agent 📍") as demo:
    gr.Markdown("# Plan your day or activity and get tips and relevant information!")
    with gr.Row():
        with gr.Column(scale=3):
            chat = gr.ChatInterface(
                fn=prompt_agent,
                examples=[
                    "מתי הכי טוב לרכב מחר על אופניים ברעננה?",
                    "כדאי לי לצאת לריצה מחר בבוקר במודיעין?",
                ],
                title="Chat",
            )
        with gr.Column(scale=1):
            gr.Markdown("מאחורי הקלעים")
            logs = gr.Code(label="שימוש בכלים", language="json")


if __name__ == "__main__":
    demo.launch()
