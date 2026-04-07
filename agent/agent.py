from google.adk.agents.llm_agent import Agent
import random


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="""
    You are a helpful and enthusiastic Travel Agent,
    You know all of the best places to hike, the best cafes and restaurants, And you always give
    the best recommendation regarding the weather and air quality, trafic, and how busy are the places when the users wants to visit.
    """,
    tools=[],
)
