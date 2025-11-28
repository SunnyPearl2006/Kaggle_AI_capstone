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

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=5,
    initial_delay=0.5,  # faster initial retry
    http_status_codes=[429, 500, 503, 504]
)

# In-memory cache to avoid repeated Google searches
SCHOOL_STATS_CACHE = {}

SchoolStatAgent = Agent(
    name="School_stat_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="This agent fetches school stats and caches them to speed up repeated queries.",
    instruction="""
You are given a target school name and application type (first-year or transfer).

1. Check if the school's data exists in memory (cache). If yes, return immediately:
   - Plain-text summary (e.g., "Average GPA is 3.8, with ~5 AP/IB classes, SAT 1450, ACT 32.")
   - JSON for internal comparison.

2. If not cached:
   - Use Google Search to find: average GPA, average AP/IB classes, SAT and ACT (if available).
   - Format results as JSON and plain-text summary.
   - Store them in memory for future queries.

3. Return **both JSON and plain-text summary**, but the agent should only print the summary to the user.
   
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
