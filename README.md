# Dad's Daily Digital Twin

A personalized AI crew that generates daily heartwarming emails for your dad, powered by [crewAI](https://crewai.com). This digital twin automatically researches your daily activities, checks on your dad's well-being, and creates personalized emails that maintain your special father-daughter connection.

## What It Does

This AI crew consists of three specialized agents that work together to:

1. **Research Today's Class** - Identifies what class you have today and explains it in parent-friendly terms
2. **Research NVIDIA Stock** - Gets current stock information and market updates
3. **Draft Heartwarming Email** - Creates a personalized, loving email for your dad
4. **Format Final Email** - Formats the email in a clean, copy-ready layout

## Features

- 🤖 **Multi-Agent AI System** - Three specialized agents working in harmony
- 📧 **Personalized Emails** - Unique, heartfelt messages every day
- 📊 **Real-Time Data** - Current stock prices and market information
- 💝 **Caring Check-ins** - Asks about your dad's health and exercise habits
- 🎓 **Class Updates** - Explains your daily classes in simple terms
- 📈 **Investment Discussions** - Shares NVIDIA stock insights and asks for his thoughts

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system.

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd HW1_DigitalTwin
```

2. **Install dependencies:**
```bash
pip install -e .
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Optional: Serper API for web search (if you want to use it)
SERPER_API_KEY=your-serper-api-key-here
```

## Quick Start

**Generate a daily email for your dad:**

```bash
cd src
python3 generate_email.py
```

This will:
- Run the AI crew
- Generate a personalized email
- Save it to `email_output.txt`
- Display the email in the terminal

## Running the Project

**Option 1: Generate Email (Recommended)**
```bash
cd src
python3 generate_email.py
```

**Option 2: Run Crew Directly**
```bash
cd src
python3 -m dad_s_daily_digital_twin.main run
```

**Option 3: Using CrewAI CLI**
```bash
crewai run
```

## Understanding Your Crew

The Dad's Daily Digital Twin crew consists of three specialized AI agents:

### 🤖 **Information Collector**
- **Role**: Researches your daily class and NVIDIA stock information
- **Tools**: ScrapeWebsiteTool for real-time data
- **Tasks**: 
  - Identifies today's class from your weekly schedule
  - Explains the class in parent-friendly terms
  - Researches current NVIDIA stock price and news

### 💝 **Heartwarming Email Writer**
- **Role**: Creates personalized, loving emails
- **Skills**: Emotional intelligence, personal communication
- **Tasks**:
  - Drafts heartfelt emails using collected information
  - Asks caring questions about your dad's health
  - Maintains your authentic voice and relationship tone

### 📧 **Email Formatter**
- **Role**: Formats emails for easy copying and sending
- **Skills**: Clean formatting, professional presentation
- **Tasks**:
  - Formats the email in a clean, copy-ready layout
  - Ensures proper structure with TO, SUBJECT, and content
  - Makes it easy to copy and send to your dad

## Customization

You can customize the crew by modifying:

- **`config/agents.yaml`** - Agent personalities and capabilities
- **`config/tasks.yaml`** - Task descriptions and requirements
- **`crew.py`** - Agent tools and configurations
- **`main.py`** - Input parameters and crew execution

## Example Output

The crew generates emails like this:

```
TO: dad@example.com
SUBJECT: Daily Update from Rebecca ❤️

Dear Dad,

I hope this email finds you well! Today I had my Deep Learning class, 
and it was absolutely fascinating! We dove into how computers can learn 
from data, much like how we humans learn from our experiences...

[Personal class update, health check-in, and investment discussion]
```

## Project Structure

```
HW1_DigitalTwin/
├── src/
│   ├── dad_s_daily_digital_twin/
│   │   ├── config/
│   │   │   ├── agents.yaml      # Agent configurations
│   │   │   └── tasks.yaml       # Task definitions
│   │   ├── crew.py              # Main crew definition
│   │   └── main.py              # Entry point
│   └── generate_email.py        # Email generation script
├── .env                         # Environment variables
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Dependencies

- **crewai[tools]** - Multi-agent AI framework
- **python-dotenv** - Environment variable management
- **ScrapeWebsiteTool** - Web scraping for real-time data

## Support

For support, questions, or feedback:
- Visit [crewAI documentation](https://docs.crewai.com)
- Check the [crewAI GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join the Discord community](https://discord.com/invite/X4JWnZnxPb)

---

**Made with ❤️ for keeping family connections strong through AI**
