import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Load credentials
load_dotenv()
SERPER_KEY = os.getenv("SERPER_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")

# 1) Initialize Gemini LLM
llm = LLM(
    model="perplexity/sonar-deep-research",
    base_url="https://api.perplexity.ai/",
    api_key=PERPLEXITY_KEY,
    temperature=0.7
)

# 2) Setup tools with HF embedder override
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
search_tool = SerperDevTool(api_key=SERPER_KEY)
web_rag_tool = WebsiteSearchTool(
    llm=llm,
    config={
        "embedder": {
            "provider": "huggingface",
            "config": {"model": EMBED_MODEL}
        }
    }
)

def fetch_market_data(product_idea):
    """
    Gather top 5–10 products for product_idea including:
    name, pricePoint, rating, reviewSummary, reviewSummaries (list).
    """
    agent = Agent(
        role="E-commerce Researcher",
        goal=f"Fetch top products data for '{product_idea}' with reviews.",
        backstory="Expert at mining product info into clean JSON.",
        tools=[search_tool, web_rag_tool],
        llm=llm,
        verbose=False
    )
    task = Task(
        description=(
            f"Find the top 5–10 products for '{product_idea}' on Amazon, Walmart, etc. "
            "For each, return a JSON object with keys: ['name', 'pricePoint', 'rating', 'reviewSummary', 'reviewSummaries'], "
            "where reviewSummaries is a list of 2-3 brief customer review snippets."
        ),
        expected_output="A JSON array of product dicts.",
        agent=agent,
        llm=llm
    )
    crew = Crew(agents=[agent], tasks=[task], planning=False, verbose=False)
    output = crew.kickoff()

    # Extract raw text
    raw = output.text if hasattr(output, 'text') else str(output)

    # Parse JSON
    try:
        start, end = raw.find('['), raw.rfind(']')
        blob = raw[start:end+1] if start!=-1 and end!=-1 else raw
        data = json.loads(blob)
    except Exception as e:
        print(f"[MarketDataAgent] JSON parse error: {e}")
        first = raw.splitlines()[0][:200]
        data = [{
            'name': first,
            'pricePoint': 'N/A',
            'rating': None,
            'reviewSummary': '',
            'reviewSummaries': []
        }]

    # Normalize and ensure fields
    for idx, item in enumerate(data, start=1):
        item.setdefault('id', idx)
        item.setdefault('reviewSummary', '')
        item.setdefault('reviewSummaries', [])
    return data
