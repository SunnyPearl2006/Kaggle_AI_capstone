import os
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from google.genai import types
from dotenv import load_dotenv
from agents.SchoolStatAgent import SchoolStatAgent

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Please set GOOGLE_API_KEY before running this script.")

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=5,
    initial_delay=0.5,
    http_status_codes=[429, 500, 503, 504]
)

# Safe constants
APP_NAME = "agents"

# Agent definition
CollegeAgent = Agent(
    name="College_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="""
You are a college adviser AI. 

1. Always remember user stats and previously queried schools per session.
2. When user mentions a school, auto-check if it's first-year or transfer.
3. For **first-year applicants**, request:
   - High school GPA (if user has not already given it to you)
   - SAT/ACT scores (if user has not already given it to you)
   - AP/IB classes (if user has not already given it to you)
4. For **transfer applicants**, request:
   - College GPA (if user has not already given it to you)
   - Number of completed credits (if user has not already given it to you)
   - Optional: GPA in major-related courses (if user has not already given it to you)
5. For each school:
   - If stats are cached, use them.
   - Otherwise, call SchoolStatAgent and cache results automatically.
6. Compare user's stats with the school's averages and classify as reach, target, or safety.
7. End conversation only when user shows intention to leave, to do this, add a final token: 
__end_conversation__
Add nothing else
8. All user inputs should be interpreted intelligently; do not ask for repeated info.
9. Do not send function calls / json to users. Those are internal to you.
""",
    tools=[AgentTool(agent=SchoolStatAgent)],
)
