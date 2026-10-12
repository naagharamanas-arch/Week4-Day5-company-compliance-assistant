
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow

# Permissions needed for Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Start Google OAuth login
flow = InstalledAppFlow.from_client_secrets_file(
    "google_oauth_credentials.json",
    SCOPES
)

credentials = flow.run_local_server(port=0)

# Connect to Google Sheets
client = gspread.authorize(credentials)

print("Google OAuth login successful!")

# Open the spreadsheet by its exact name
spreadsheet = client.open("Company Compliance Audit Log")

print("Spreadsheet opened successfully!")
print("Spreadsheet title:", spreadsheet.title)
