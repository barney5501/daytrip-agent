from google.adk.agents.llm_agent import Agent
import random


# mock
def get_air_quality(city: str, date: str) -> dict:
    """
    Returns the air quality in a city at a specified date.
    the rating scale is 0 to 5
    0 - POOR
    1 - VERY BAD
    2 - BAD
    3 - OKAY
    4 - GOOD
    5 - GREAT
    """
    return {"status": "success", "city": city, "air_quality_rate": random.randint(1, 5)}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="""
    You are a helpful and enthusiastic Travel Agent,
    You know all of the best places to hike, the best cafes and restaurants, And you always give
    the best recommendation regarding the weather and air quality, trafic, and how busy are the places when the users wants to visit.
    """,
    tools=[get_air_quality],
)
