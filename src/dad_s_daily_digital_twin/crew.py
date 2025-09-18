import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool
)




@CrewBase
class DadSDailyDigitalTwinCrew:
    """DadSDailyDigitalTwin crew"""

    
    @agent
    def heartwarming_email_writer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["heartwarming_email_writer"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def information_collector(self) -> Agent:

        
        return Agent(
            config=self.agents_config["information_collector"],
            
            
            tools=[
				ScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def email_formatter(self) -> Agent:

        
        return Agent(
            config=self.agents_config["email_formatter"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def research_today_s_class(self) -> Task:
        return Task(
            config=self.tasks_config["research_today_s_class"],
            markdown=False,
            
        )
    
    @task
    def research_nvidia_stock(self) -> Task:
        return Task(
            config=self.tasks_config["research_nvidia_stock"],
            markdown=False,
            
        )
    
    @task
    def draft_heartwarming_email(self) -> Task:
        return Task(
            config=self.tasks_config["draft_heartwarming_email"],
            markdown=False,
            
        )
    
    @task
    def format_final_email(self) -> Task:
        return Task(
            config=self.tasks_config["format_final_email"],
            markdown=False,
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the DadSDailyDigitalTwin crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

