# 🧠 LLM Inference Leaderboard & Analytics

This is a project I’m working on with **Vaughn DiMarco**, who’s building a startup that wants to bring a BECK-style system (like what’s used in crypto) into the LLM space. The core idea is to eventually let people **track, evaluate, and even trade LLM model tokens** — kind of like a performance marketplace for AI models.

We’re starting by collecting and analyzing **real-time inference data** from platforms like [OpenRouter.ai](https://openrouter.ai) and Shoots.ai, then building a **leaderboard** to make that data public and trustable.

---

## 🚀 What We’re Trying to Do

We’re looking to make LLM usage and performance transparent. Specifically, we want to track:

- How many inferences each model/provider is doing
- How many tokens are being generated
- How much those inferences are costing
- Who’s providing what
- Which models are most efficient or popular

Eventually, the goal is to **publish this data in a public leaderboard** that people can filter and explore.

---

## 📊 Key Features (In Progress)

- Total number of inferences
  - Hourly, daily, etc. (based on what the API provides)
- Tokens generated over time
- Real-time **cost per token**
  - Updated minute by minute
- Filterable data:
  - ⏱️ Time
  - 💰 Price
  - 🔢 Token usage
  - 🧠 Model name
  - 🏢 Provider name

---

## 🛠️ How I’m Getting the Data

Originally tried using the OpenRouter API (and even used an LLM to parse the responses), but the results weren’t great — some data was missing or unstructured.

So I pivoted to **scraping** the site using **BeautifulSoup + Selenium** to get more consistent results. Right now it’s pulling info like:

- Provider names
- Associated LLM models
- Inference cost & token-related data (still improving this)

Also exploring **Shoots.ai** as a potential secondary data source.

---

## ✅ What’s Done So Far

- Scraper built for OpenRouter using BeautifulSoup + Selenium
- Extracted provider/model pairs
- Tested early attempts at getting cost and token info
- Project structured for future automation

---

## 🔜 What’s Coming Next

- Improve scraping to capture live token + pricing data
- Store hourly/daily snapshots of inference usage
- Build a basic leaderboard frontend (thinking Streamlit or lightweight web app)
- Add full filtering (by time, model, tokens, provider, etc.)
- Pull in additional sources like Shoots.ai if useful

---

## 📁 Project Structure

```bash
llm-inference-project/
├── scrapers/       # Web scraping scripts (OpenRouter, Shoots.ai)
├── data/           # Stored results (JSON, CSV, etc.)
├── notebooks/      # Exploratory analysis / quick data viz
├── scripts/        # Utilities for parsing, formatting, etc.
└── README.md       # This file
