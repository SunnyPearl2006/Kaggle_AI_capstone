# gather all the required imports
# use asyncio so flow is not paused or stopped
import asyncio
import uuid
from google.adk.runners import InMemoryRunner
from agents.CollegeAgent import CollegeAgent, APP_NAME
from google.genai import types

# define main, which will create session and add it to memory
async def main():
    # Runner with memory, only up to session memory, cannot 
    # remember between sessions
    runner = InMemoryRunner(agent=CollegeAgent, app_name=APP_NAME)

    # Create user/session
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )
    # Store the session in the runner's in-memory storage (only lasts for this run)
    await runner.memory_service.add_session_to_memory(session)

    # define message function
    async def send_message(user_text):
        # define what the user sent
        content = types.Content(role="user", parts=[types.Part(text=user_text)])
        # print out what college agent said
        async for evt_tuple in runner.run_async(user_id=session.user_id, session_id=session.id, new_message=content):
            event = evt_tuple[0] if isinstance(evt_tuple, tuple) else evt_tuple
            if getattr(event, "content", None) and getattr(event.content, "parts", None):
                # makes sure it does not freeze after a function call.
                if not getattr(event, "content", None):
                    continue
                # added or [] so it does not crash when empty
                for part in event.content.parts or []:
                    
                    text = getattr(part, "text", None)
                    if text:
                        # check if convo has been ended by agent
                        print("College Agent:", text.strip())
                        if "__end_conversation__" in text:
                            return True
                    elif getattr(part, "function_call", None):
                        print("College Agent (function call / JSON):", part.function_call)
        return False

    # Intro message to start the ai
    await send_message("__start__")

    # Conversation loop
    while True:
        user_input = input().strip()
        if not user_input:
            continue
        # If the agent signals that the conversation ended, exit the loop
        if await send_message(user_input):
            break

if __name__ == "__main__":
    # run main async
    asyncio.run(main())
