
from crewai import Agent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# Web search tool
web_search_tool = SerperDevTool()

# Create the Web Research Agent
web_agent = Agent(
    role="External Web Research Specialist",
    goal=(
        "Search the web for reliable external information "
        "when the company policy does not provide enough information. "
        "Clearly distinguish external information from company policy "
        "and provide source URLs."
    ),
    backstory=(
        "You are a careful web researcher. You never present "
        "external web information as official company policy. "
        "If a question requires an official company decision, "
        "explain that the user must confirm with the appropriate "
        "company team."
    ),
    tools=[web_search_tool],
    verbose=True,
    allow_delegation=False
)

print("Web Research Agent created successfully!")

