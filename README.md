# MarketMinds 🧠📊

**MarketMinds** is an AI-powered web application designed to simplify and automate product and market research. It leverages autonomous AI agents to provide actionable insights, competitor analysis, and strategic recommendations—all in one unified interface.

[![MarketMinds](MarketMinds.png)](https://github.com/Aniket25042003/MarketMinds)


---

## 🚀 Features

- 🔍 **Product Insight**  
  Explore detailed product descriptions, specs, and metadata.

- 📊 **Competitor Pricing Analysis**  
  Compare real-time pricing across major competitors.

- 🗣️ **Customer Review Summarization**  
  Get key sentiment themes from real customer feedback.

- 🕳️ **Market Gap Identification**  
  Detect missing features or underserved market segments.

- 🧭 **Strategic Recommendations**  
  AI-generated ideas for positioning, marketing, or product enhancements.

---

## 🤖 AI Architecture

MarketMinds uses **CrewAI Tools** to coordinate multiple autonomous AI agents, each responsible for a part of the market research workflow:

- `ProductAgent` – Extracts and summarizes key product info
- `CompetitorAgent` – Scrapes and compares competitor offerings
- `ReviewAgent` – Analyzes customer reviews and sentiment
- `StrategistAgent` – Synthesizes findings into strategic suggestions

### 🧠 LLM Backend

These agents are powered by **Google's Gemini model**, which enables contextual reasoning, context understanding, and strategy generation.

---

## 🛠️ Tech Stack

- 𝐅𝐫𝐨𝐧𝐭𝐞𝐧𝐝: React, Tailwind CSS
- 𝐁𝐚𝐜𝐤𝐞𝐧𝐝: FastAPI
- 𝐀𝐈 𝐋𝐚𝐲𝐞𝐫: CrewAI + LangChain + custom LLM pipelines
- 𝐀𝐏𝐈𝐬: SerpAPI for live product data

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Aniket25042003/MarketMinds.git
cd MarketMinds
```
### 2. Install Dependecies
#### Frontend
```bash
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Demo
https://drive.google.com/file/d/14hr-pNckJuonnD9jCAgYL5rkhO2PQ9Wk/view?usp=sharing

## License
This project is open-source and available under the MIT License.

## 🙋‍♂️ Author
**Aniket Patel**  
Computer Science @ Ashland University  

[LinkedIn](https://www.linkedin.com/in/aniketpatel2003/) | [GitHub](https://github.com/Aniket25042003)


## Tags
AI Agents • Gemini LLM • CrewAI • Market Research • FastAPI • React • LangChain • Product Analytics
