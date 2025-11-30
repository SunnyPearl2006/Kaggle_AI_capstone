Problem Statement:
Often, when a person in college or high school want to figure out what their chances are at a certain college. They face three options, go to multiple websites and read through entire articles
which might be behind a paywall it self, go to an expensive coach to figure out your chances, or sign up for an AI. Majority of the time, no one wants to pay thousands of dollars for a coach
or have a reading session to figure out their chances. Sometimes the person doesn't want to sign up for an AI because of personal reasons.
Solution Statement:
An agent can give you a good picture of your chances without having to read through an article or pay thousands of dollars for an coach or pay for a paywalled website. This is where my ai agent 
comes in, it uses a sub agent to gather your target schools acadmeic stats, with the sub agent itself returing the stats based on application type, making sure you get the best results.
Architecture:
This is built off of python 3.11.14 and the google adk kit. The rest of the requirements are listed in requirements.txt. It is for now command line based.
CollegeAgent:
  This is the main agent. It first gets the user stats and stores the info in its memory and uses SchoolStatAgent to get the required info about the school. It compares the two and tells the 
  user if it is a reach, target, or safety.
SchoolStatAgent:
  This is a subagent. It uses google search tool to get the info about the school and returns both a plain text summery and a json to the main agent.
Installation:
  This project was built against Python 3.11.14. 
  Install dependenies e.g. pip install -r requirements.txt
Project Structure:
The agents are in the agents folder and main is outside.
Workflow:
1. CollegeAgent will introduce himself and ask for the school, aplication type and the revelent stats.
2. It will call SchoolStatAgent to get the school's info
3. It will compare and tell the user what it thinks the user chances are.
4. If the user shows intent to leave, CollegeAgent will end the session, otherwise the session will keep going
