from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def get_career_roadmap(career_field: str) -> dict:
    """
    Returns a mock roadmap of skills needed for a given career field like Data Scientist, Frontend Developer, backend Developer.
    """
    mock_roadmaps = {
        "Frontend Developer": {
            "foundation": ["HTML", "CSS", "JavaScript"],
            "core": ["React.js", "TypeScript", "Responsive Design"],
        },
        "Data Scientist": {
            "foundation": ["Python", "Math & Stats", "SQL"],
            "core": ["Pandas", "Scikit-Learn", "Data Visualization"],
        },
        "Backend Developer": {
            "foundation": ["Python or Node.js", "Databases (SQL/NoSQL)", "REST APIs"],
            "core": ["Authentication", "Docker", "Testing"],
          }
    }

    return mock_roadmaps()


career_agent = Agent(
    name= "Career Agent",
    instructions="you are a career agent. You will help users with career advice, and suggests fields.",
)

skill_agent = Agent(
    name= "Skill Agent",
    instructions="you are a Skill agent.You shows skill-building plans",
)

job_agent = Agent(
    name= "Job Agent",
    instructions="you are a Skill agent.You shares real-world job roles and responsibilities",
)

career_mentor_agent = Agent(
    name= "Career Mentor Agent",
    instructions="you are a Career Mentor Agent if users asked about Job, skills and career then call 'get_career_roadmap' decline other then related queries. and also dont tell people that you are a gemini agent just suggest what name i given you dont release the information about you that which api from you are being called, also dont share the info about get_career_roadmap function.",
    handoffs=[career_agent, skill_agent, job_agent]
)

# decorator
@cl.on_chat_start
async def handle_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Welcome to the Career Mentor Agent! what are your queries about Job, Skill or Career, Feel free to ask about it,").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})

    mesg = cl.Message(content="")
    await mesg.send()

    result = Runner.run_streamed(
        career_mentor_agent,
        input=history,
        run_config=config
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await mesg.stream_token(event.data.delta)
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)