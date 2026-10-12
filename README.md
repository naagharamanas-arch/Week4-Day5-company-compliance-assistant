# Company Policy & Compliance Assistant

## Project Overview

The Company Policy & Compliance Assistant is an AI-powered application that answers employee questions using company policy documents. If the available policy does not contain sufficient information, the application uses a Web Research Agent to find external information and clearly distinguishes it from official company policy.

## Features

- **RAG (Retrieval-Augmented Generation):** Searches company policy documents for relevant information.
- **Policy Agent:** Answers questions using retrieved company policy information.
- **Web Research Agent:** Searches for external information when the policy is insufficient.
- **Source Links:** Extracts external URLs from the research response.
- **Google Sheets Audit Log:** Records employee questions, policy results, agent usage, final answers, source links, and status.
- **Multi-Agent Workflow:** Routes questions between the Policy Agent and Web Research Agent.

## Technologies Used

- Python
- CrewAI
- ChromaDB
- LangChain
- OpenAI
- Serper Web Search
- Google Sheets API
- gspread

## Project Workflow

1. The employee enters a question.
2. The Policy Agent searches the company policy knowledge base.
3. If the policy provides an answer, the application returns it.
4. If the policy is insufficient, the Web Research Agent searches external sources.
5. External information and source links are returned separately from official company policy.
6. The application records the result in Google Sheets.

## Audit Log Fields

- Timestamp
- Employee Question
- Policy Result
- Web Agent Used
- Final Answer
- Source Links
- Status

## Sample Policy Questions

**Policy-based question:**  
Can employees upload customer data to personal cloud storage?

**External research question:**  
What is the company's annual employee training budget?

## Important Note

The policy document used in this learning project is a fictional sample. External web research is not official company policy. Actual company decisions must be confirmed with the appropriate internal department.

## Project Status

Core policy retrieval, agent routing, external web research, and Google Sheets audit logging have been tested successfully.