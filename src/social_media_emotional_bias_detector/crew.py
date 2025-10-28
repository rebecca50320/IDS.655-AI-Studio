import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task







@CrewBase
class SocialMediaEmotionalBiasDetectorCrew:
    """SocialMediaEmotionalBiasDetector crew"""

    
    @agent
    def social_media_content_processor(self) -> Agent:

        
        return Agent(
            config=self.agents_config["social_media_content_processor"],
            
            
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
    def cognitive_bias_emotion_analyzer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["cognitive_bias_emotion_analyzer"],
            
            
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
    def process_social_media_content(self) -> Task:
        return Task(
            config=self.tasks_config["process_social_media_content"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_emotional_bias_and_algorithmic_impact(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_emotional_bias_and_algorithmic_impact"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SocialMediaEmotionalBiasDetector crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
