# sentiment_agent.py

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

def analyze_sentiment(market_data):
    """
    Uses a CrewAI Agent to classify each review snippet in market_data
    into positive or negative themes.
    Returns {"positive": [...], "negative": [...]}.
    """
    # 1) Gather all snippets
    reviews = []
    for item in market_data:
        for rev in item.get("reviewSummaries", []):
            if isinstance(rev, str) and rev.strip():
                reviews.append(rev.strip())
        main = item.get("reviewSummary")
        if isinstance(main, str) and main.strip():
            reviews.append(main.strip())

    # Dedupe but keep order
    seen = set()
    unique_reviews = []
    for r in reviews:
        if r not in seen:
            seen.add(r)
            unique_reviews.append(r)

    # If empty, add a placeholder to trigger JSON structure
    if not unique_reviews:
        unique_reviews = ["No user reviews available."]

    # 2) Build context JSON
    context = {"reviews": unique_reviews}
    context_json = json.dumps(context, indent=2)

    # 3) Create sentiment-analyst agent
    analyst = Agent(
        role="Sentiment Analyst",
        goal="Classify review snippets into positive and negative themes.",
        backstory="Expert linguist distilling customer feedback into clear sentiment categories.",
        tools=[],  # no external tools needed
        llm=llm,
        verbose=False
    )

    # 4) Define the Task with explicit JSON schema
    prompt = (
        f"You are a sentiment analyst. Here is your data:\n\n{context_json}\n\n"
        "Please output **only** a single JSON object with two keys:\n"
        "  1) \"positive\": an array of review snippets that express positive sentiment.\n"
        "  2) \"negative\": an array of review snippets that express negative sentiment.\n\n"
        "**Do not** include any additional keys, commentary, or formatting—just the JSON."
    )
    task = Task(
        description=prompt,
        expected_output=(
            '{"positive":["...","..."],"negative":["...","..."]}'
        ),
        agent=analyst,
        llm=llm
    )

    # 5) Run the Crew
    crew = Crew(
        agents=[analyst],
        tasks=[task],
        planning=False,
        verbose=False
    )
    result = crew.kickoff()

    # 6) Extract raw output and log
    raw = result.text if hasattr(result, "text") else str(result)

    # 7) Isolate JSON block
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_blob = raw[start:end+1]
    else:
        json_blob = raw

    # 8) Parse JSON
    try:
        parsed = json.loads(json_blob)
        positive = parsed.get("positive", [])
        negative = parsed.get("negative", [])
    except Exception as e:
        positive, negative = [], []

    return {"positive": positive, "negative": negative}
