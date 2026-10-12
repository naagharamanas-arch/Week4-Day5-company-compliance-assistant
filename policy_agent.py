from crewai import Agent, Task, Crew
from crewai.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Connect to the existing company policy database
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Search only the company policy documents
@tool("Search Company Policy")
def search_company_policy(question: str) -> str:
    """Search company policy documents for relevant information."""
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    if not results:
        return "The available company policy does not contain sufficient information."

    return "\n\n".join(
        doc.page_content for doc in results
    )


# Create the Policy Agent
policy_agent = Agent(
    role="Company Policy Compliance Specialist",
    goal=(
        "Answer employee questions using only the retrieved "
        "company policy information. Never invent company rules. "
        "If the policy does not provide enough information, "
        "clearly say so."
    ),
    backstory=(
        "You are a careful compliance assistant. "
        "You must rely only on the company policy information "
        "provided to you and must not use external web information "
        "as company policy."
    ),
    tools=[search_company_policy],
    verbose=True,
    allow_delegation=False
)

print("Policy Agent created successfully!")


policy_task = Task(
    description=(
        "Answer this employee question using only the company "
        "policy search tool: {question}. "
        "If the retrieved policy does not provide enough information, "
        "say that the available company policy does not contain "
        "sufficient information. Do not use outside knowledge."
    ),
    expected_output=(
        "A concise answer based only on retrieved company policy, "
        "or a clear statement that the policy information is insufficient."
    ),
    agent=policy_agent
)

policy_crew = Crew(
    agents=[policy_agent],
    tasks=[policy_task],
    verbose=True
)

if __name__ == "__main__":
    result = policy_crew.kickoff(
        inputs={
            "question": "Can employees upload customer data to personal cloud storage?"
        }
    )
    print("\nFINAL POLICY ANSWER:\n", result)
