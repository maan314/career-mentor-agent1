🎓 Career Mentor Agent
An intelligent, multi-agent career guidance assistant built using Chainlit, OpenAI Agent SDK, Gemini API, and UVicorn.

🚀 What It Does
The Career Mentor Agent helps users explore career paths, understand required skills, and discover relevant job roles using structured agent handoff and actionable insights.

🧠 Key Features
Multi-Agent Support with Handoff:

🎯 CareerAgent: Recommends career fields based on user interests

🧠 SkillAgent: Identifies key skills and learning paths using get_career_roadmap()

💼 JobAgent: Shows real-world job roles aligned with the selected career

Tool Integration:

get_career_roadmap() — returns mock data of skills required in specific careers

Smooth Agent Handoff: Dynamically passes the conversation between agents depending on user needs (e.g., field → skills → jobs)

Conversational UI: Delivered with Chainlit for real-time interaction

🛠️ Tech Stack
⚙️ OpenAI Agent SDK

🧩 Chainlit – Conversational interface

🔁 Gemini API – Contextual reasoning

⚡ UVicorn – Fast ASGI server

🧪 Mock Tool Data – Simulated backend responses

🧪 Example Use Case
User: I'm interested in working in data science.
CareerAgent: Great! Data Science is a top choice.
Handoff → SkillAgent
SkillAgent: To succeed in Data Science, you’ll need Python, Machine Learning, and SQL.
Handoff → JobAgent
JobAgent: Here are job roles: Data Analyst, Machine Learning Engineer, and AI Specialist.