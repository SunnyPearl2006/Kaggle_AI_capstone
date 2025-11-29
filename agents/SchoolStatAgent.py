# gather all the required imports
import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Please set GOOGLE_API_KEY before running this script.")

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=5,
    initial_delay=0.5,  # faster initial retry
    http_status_codes=[429, 500, 503, 504]
)

# Agent definition
# tell it to use google search to get stats about school
# tell it to return results in json for easy parsing
SchoolStatAgent = Agent(
    name="School_stat_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="This agent fetches school stats and caches them to speed up repeated queries.",
    instruction="""
                You are given a target school name and application type (first-year or transfer).

                1. Search for the school's data and:
                 - if application is transfer, only get average transfer gpa and the average number
                 of completed college credits and if possible average gpa in major related courses.
                 if you cannnot find it, set that field to not found in the json, do not leave it empty.
                 - if application is first year, get:
                    - Average admited GPA
                    - Average admited SAT/ACT scores
                    - Average admited AP/IB classes
                if you cannnot find it, set that field to not found in the json, do not leave it empty.



                2. Return **both JSON and plain-text summary**, but the agent should only print the summary to the user.
   
                Example JSON output:
                {
                    "Average GPA": "3.8",
                    "Average AP_IB_classes": 5,
                    "Average SAT score": 1450,
                    "Average ACT score": 32
                }
                Example text summary:
                "The average GPA is 3.8, with around 5 AP/IB classes, average SAT 1450, and ACT 32."
                """,
    tools=[google_search]
)
