import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from langchain_groq import ChatGroq

# Model ID verified directly from your Groq key
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)


def research_agent(state):
    topic = state.get("topic", "")
    prompt = f"Provide brief key research facts and key points about the topic: {topic}"
    response = llm.invoke(prompt)
    return {"research_notes": response.content, "current_step": "Research done"}


def planner_agent(state):
    research_notes = state.get("research_notes", "")
    prompt = f"Create a structured article outline based on these research notes:\n\n{research_notes}"
    response = llm.invoke(prompt)
    return {"outline": response.content, "current_step": "Planner done"}


def writer_agent(state):
    topic = state.get("topic", "")
    outline = state.get("outline", "")
    prompt = f"Write a comprehensive article titled '{topic}' based on this outline:\n\n{outline}"
    response = llm.invoke(prompt)
    return {"final_content": response.content, "current_step": "Writer done"}