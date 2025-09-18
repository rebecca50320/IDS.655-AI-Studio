# Daily Digital Twin for Dad

A crewAI powered AI crew that researches your day and drafts a daily, heartwarming email for your dad. It checks in on his well-being, summarizes your classes, and adds simple market context such as NVIDIA stock.

## What It Does

The crew has three agents working together:

1. **Information Collector**

   * Finds today’s class and explains it in parent friendly terms
   * Retrieves current NVIDIA price and brief market context

2. **Heartwarming Email Writer**

   * Drafts a personalized message in your voice
   * Includes caring check-ins about health and exercise

3. **Email Formatter**

   * Produces a clean, copy ready layout with TO and SUBJECT

## Features

* Multi-agent flow with clear roles
* Personalized daily emails
* Current class and market snippets
* Caring prompts for dad’s well-being
* Simple outputs to file and terminal

## Installation

Python version should be at least 3.10 and below 3.14.

1. **Clone**

```bash
git clone <your-repo-url>
cd HW1_DigitalTwin
```

2. **Install**

```bash
pip install -e .
```

3. **Environment**
   Create a `.env` in the project root:

```bash
# OpenAI
OPENAI_API_KEY=your-openai-api-key-here
```

## Quick Start

Generate today’s email:

```bash
cd src
python3 generate_email.py
```

This runs the crew, saves `email_output.txt`, and prints the result.

### Alternative Ways to Run

```bash
# Module entry point
cd src
python3 -m dad_s_daily_digital_twin.main run

# CrewAI CLI
crewai run
```

## Understanding Your Crew

* **Information Collector**
  Tools: ScrapeWebsiteTool for class and market lookups

* **Heartwarming Email Writer**
  Skills: simple tone control and personalization

* **Email Formatter**
  Output: copy ready structure with subject line

## Customization

* `config/agents.yaml` for personalities and tools
* `config/tasks.yaml` for task prompts
* `crew.py` for tool wiring
* `main.py` for inputs and execution


## Project Structure

```
HW1_DigitalTwin/
├── src/
│   ├── dad_s_daily_digital_twin/
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   ├── crew.py
│   │   └── main.py
│   └── generate_email.py
├── .env
├── pyproject.toml
└── README.md
```

## Dependencies

* `crewai[tools]`
* `python-dotenv`
* `ScrapeWebsiteTool`


## Implementation Notes

 1. **Fetching current stock price**

**Tried:** SerpAPI Google Finance; returned 403 Unauthorized.  
**Decision:** Switched to `ScrapeWebsiteTool` to read a Google Finance or Yahoo Finance quote card.  
**Status:** Works for the MVP; scraping is brittle if page structure changes and quotes may be delayed.  


 2. **Email delivery**

**Issue:** Gmail authorization was not completing during setup.  
**Decision:** Generate `email_output.txt` and print to terminal for manual send.  
**Status:** Reliable for daily use.  

**Workflow disclosure**: Prototype in CrewAI browser -> Implement and test locally in Cursor -> Push to GitHub

## Support

* [crewAI docs](https://docs.crewai.com)
* [crewAI GitHub](https://github.com/joaomdmoura/crewai)
* [Discord](https://discord.com/invite/X4JWnZnxPb)

---

**Made with ❤️ to keep family connections strong**
