# competitor_agent.py

import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")

llm = LLM(
    model="perplexity/sonar-reasoning-pro",
    base_url="https://api.perplexity.ai/",
    api_key=PERPLEXITY_KEY,
    temperature=0.7
)

def analyze_competitors(market_data, product_idea):
    """
    Uses a CrewAI Agent to summarize competitors in a single sentence.
    Returns the market_data list with 'summary' injected on the first item.
    """
    # 1) Build context JSON
    context = {
        "productIdea": product_idea,
        "competitors": market_data
    }
    context_json = json.dumps(context, indent=2)

    # 2) Create competitor-analyst agent
    analyst = Agent(
        role="Competitor Analyst",
        goal="Summarize key competitors, their unique features, strengths & weaknesses. Include both positive and negative aspects.",
        backstory="A market researcher skilled at distilling product comparisons into concise summaries.",
        tools=[],
        llm=llm,
        verbose=False
    )

    # 3) Define JSON-only output task
    prompt = (
        f"You are a competitor analyst. Here is your data:\n\n{context_json}\n\n"
        "Output **only** a JSON object with a single key:\n"
        "  \"summary\": a concise paragraph (1–2 sentences) capturing the key competitors, "
        "their unique features, and notable strengths/weaknesses.\n"
        "Include both positive and negative aspects.\n"
        "Do not include any other keys or commentary."
    )
    task = Task(
        description=prompt,
        expected_output='{"summary":"…"}',
        agent=analyst,
        llm=llm
    )

    # 4) Run Crew
    crew = Crew(agents=[analyst], tasks=[task], planning=False, verbose=False)
    result = crew.kickoff()

    # 5) Debug raw output
    raw = result.text if hasattr(result, "text") else str(result)
    
    # 6) Extract JSON blob
    start, end = raw.find("{"), raw.rfind("}")
    blob = raw[start:end+1] if start != -1 and end != -1 else raw

    # 7) Parse JSON
    try:
        parsed = json.loads(blob)
        summary = parsed.get("summary", "").strip()
    except Exception as e:
        summary = ""

    # 8) Attach to first competitor
    competitors = [{**item} for item in market_data]
    if competitors:
        competitors[0]["summary"] = summary

    return competitors
