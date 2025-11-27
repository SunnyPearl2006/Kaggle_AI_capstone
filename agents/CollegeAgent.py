import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv
import asyncio

# Make sure your API key is set in the environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Please set GOOGLE_API_KEY before running this script.")
else:
    print("Got key!")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

College_agent = Agent(
    name="College_adviser",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="This agent uses subagents to tell the user what their chances are at a certain college.",
    instruction="You are a college adviser. Currently, you are being tested. Ask the user which college they want to attend and whether they are applying as a first-year or transfer student. Then use the Google Search tool to gather accurate information about the college based on their response and respond to user with that information. Include acadamic stats.",
    tools=[google_search],
)


