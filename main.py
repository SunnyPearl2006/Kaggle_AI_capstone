# main.py
import asyncio
import uuid
from agents.CollegeAgent import College_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def main():
    runner = InMemoryRunner(agent=College_agent, app_name="agents")

    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )

    print("✅ College Agent started. Type 'quit, exit, or bye' to exit.\n")

    while True:
        user_text = input("\n").strip()
        if user_text.lower() in ("quit", "exit", "bye"):
            print("Ending session.")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_text)])

        # Use run_async + async for instead of run() to avoid loop issues
        try:
            async for evt_tuple in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content
            ):
                event = evt_tuple[0] if isinstance(evt_tuple, tuple) else evt_tuple
                if getattr(event, "content", None) and getattr(event.content, "parts", None):
                    for part in event.content.parts:
                        print()
                        print("College Agent:", part.text)
                        print()
        except Exception as e:
            print("Error communicating with agent:", e)

# Proper single asyncio.run call
if __name__ == "__main__":
    asyncio.run(main())
