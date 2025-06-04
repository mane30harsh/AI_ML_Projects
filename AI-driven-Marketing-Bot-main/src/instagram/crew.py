from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from instagram.tools.search import SearchTools  # Import the correct tool classes for CrewAI
from crewai.tools import tool  # Import the tool decorator instead

@CrewBase
class InstagramCrew:
    """Instagram crew"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # Define tools using the @tool decorator
    @tool("Search the internet for information")
    def search_internet(self, query: str) -> str:
        """Use this tool to search the internet for information. This tools returns 5 results from Google search engine."""
        return SearchTools.search_internet(query)
    
    @tool("Search Instagram")
    def search_instagram(self, query: str) -> str:
        """Use this tool to search Instagram. This tools returns 5 results from Instagram pages."""
        return SearchTools.search_instagram(query)
    
    @tool("Open a webpage and get the content")
    def open_page(self, url: str) -> str:
        """Use this tool to open a webpage and get the content."""
        return SearchTools.open_page(url)
    
    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            tools=[self.search_internet, self.search_instagram, self.open_page],
            verbose=True,
        )
    
    # Rest of your code remains unchanged
    @agent
    def content_strategist(self) -> Agent:
        return Agent(config=self.agents_config["content_strategist"], verbose=True)
    
    @agent
    def visual_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["visual_creator"],
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def copywriter(self) -> Agent:
        return Agent(config=self.agents_config["copywriter"], verbose=True)
    
    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.market_researcher(),
            output_file="market_research.md",
        )
    
    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_strategy"],
            agent=self.content_strategist(),
        )
    
    @task
    def visual_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["visual_content_creation"],
            agent=self.visual_creator(),
            output_file="visual-content.md",
        )
    
    @task
    def copywriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriting"],
            agent=self.copywriter(),
        )
    
    @task
    def report_final_content_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["report_final_content_strategy"],
            agent=self.content_strategist(),
            output_file="final-content-strategy.md",
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Instagram crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,  # Changed from 2 to True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )