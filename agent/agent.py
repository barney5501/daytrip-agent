from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools import available_tools

APP_NAME = "Travel Agent"
USER_ID = "user_default"
SESSION_ID = "session_01"


root_agent = Agent(
    model="gemini-3.1-flash-lite-preview",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="""
    You are a helpful and enthusiastic Travel Agent,
    You help people plan the perfect day-trips according to their preferences and using the tools you have to gather relevant outdoor information.
    Follow these strict steps:
    1. Check the weather and air quality in the requested area using your tools.
    2. Evaluate if the user's plan is aligned with the environmental conditions. For example, if a user wants to go biking and it is going to rain, explicitly acknowledge the bad weather and suggest an indoor alternative like a gym.
    3. Recommend relevant, SPECIFIC places they might enjoy, or alternative activities that fit the conditions better.
    Answer in a short form, use bullets if you list but otherwise speak naturally. Keep your answers concise, engaging, and professional.
    Always answer in Hebrew!
    """,
    tools=available_tools,
)


# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    )

    logs = ""
    async for event in events:
        if not event.is_final_response():
            calls = []
            for part in event.content.parts:
                if hasattr(part, "function_call") and part.function_call is not None:
                    part_call = f"function called: {part.function_call.name}.\npassed arguments: {part.function_call.args}\n"
                    calls.append(part_call)
            logs += "\n".join(calls)
            yield ("בוחן...", logs)
        else:
            final_response = event.content.parts[0].text
            logs += "\n\n\nתשובה סופית"
            yield (final_response, logs)
