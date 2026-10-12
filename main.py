
from crewai import Task, Crew
from policy_agent import policy_agent
from web_agent import web_agent
import gspread
from datetime import datetime
import re


def connect_google_sheet():
    client = gspread.oauth(
        credentials_filename="google_oauth_credentials.json"
    )
    spreadsheet = client.open("Company Compliance Audit Log")
    return spreadsheet.sheet1


def log_audit(question, policy_result, web_agent_used, final_answer, source_links, status):
    sheet = connect_google_sheet()

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        question,
        policy_result,
        "Yes" if web_agent_used else "No",
        final_answer,
        source_links,
        status
    ])

def answer_employee_question(question: str):
    # Step 1: Check the company policy first
    policy_task = Task(
        description=(
            "Answer this employee question using only the company "
            "policy search tool: {question}\n"
            "If the policy search results do not directly answer "
            "the question, clearly state that the available company "
            "policy does not contain sufficient information. "
            "Do not use outside knowledge."
        ),
        expected_output=(
            "A policy-based answer, or the exact statement that "
            "the available company policy does not contain "
            "sufficient information."
        ),
        agent=policy_agent
    )

    policy_crew = Crew(
        agents=[policy_agent],
        tasks=[policy_task],
        verbose=True
    )

    policy_result = policy_crew.kickoff(
        inputs={"question": question}
    )

    policy_answer = str(policy_result)
    policy_status = "Insufficient"
    web_agent_used = False
    source_links = ""
    final_answer = ""

    # Step 2: Use web research only when policy is insufficient
    if "does not contain sufficient information" in policy_answer.lower():
        print("\nPolicy information is insufficient.")
        print("Starting external web research...\n")

        web_task = Task(
            description=(
                "Research this question using web search: {question}\n"
                "Company policy does not contain sufficient information. "
                "Provide external information with source URLs. "
                "Clearly state that this is external information, "
                "not official company policy. Do not invent company rules."
            ),
            expected_output=(
                "A concise external research answer with source URLs "
                "and a clear disclaimer that it is not company policy."
            ),
            agent=web_agent
        )

        web_crew = Crew(
            agents=[web_agent],
            tasks=[web_task],
            verbose=True
        )

        web_result = web_crew.kickoff(
            inputs={"question": question}
        )

        
        web_agent_used = True
        final_answer = str(web_result)

        urls = re.findall(r'https?://[^\s)]+', final_answer)
        source_links = "\n".join(urls)

        policy_status = "External Research Completed"
        print("\nFINAL ANSWER (EXTERNAL RESEARCH):\n", final_answer)


    
    else:
        policy_status = "Answered"
        final_answer = policy_answer
        print("\nFINAL ANSWER (COMPANY POLICY):\n", final_answer)



    log_audit(
        question=question,
        policy_result=policy_answer,
        web_agent_used=web_agent_used,
        final_answer=final_answer,
        source_links=source_links,
        status=policy_status
    )
    print("\nAudit log saved to Google Sheets!")

if __name__ == "__main__":
    user_question = input("Enter your company policy question: ")
    answer_employee_question(user_question)
