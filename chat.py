import os
from flask import Flask, render_template, request
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pickle
import sys
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Enable OAuth 2.0 for local testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

print(f"Spreadsheet ID from env: {SPREADSHEET_ID}")

if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")
if not SPREADSHEET_ID:
    raise ValueError("No SPREADSHEET_ID found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini 1.5 Pro model
try:
    model = genai.GenerativeModel('models/gemini-1.5-pro')
except Exception as e:
    raise RuntimeError(f"Failed to initialize Gemini model: {e}")

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
RANGE_NAME = 'Sheet1'  # We'll read the entire sheet

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_content_with_retry(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            print("Rate limit hit, retrying after delay...")
        raise

def get_sheets_service():
    try:
        creds = None
        if os.path.exists('token.pickle'):
            print("Found existing token.pickle file")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                print("Loaded credentials from token.pickle")
        
        if not creds or not creds.valid:
            print("No valid credentials found, starting OAuth flow")
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                print("Starting new OAuth flow")
                if not os.path.exists('credentials.json'):
                    print("Error: credentials.json file not found!")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            print("Saving new credentials to token.pickle")
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        print("Building Sheets service")
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error in get_sheets_service: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {sys.exc_info()}")
        return None

def read_sheet():
    try:
        print("\n=== Starting sheet read ===")
        service = get_sheets_service()
        if not service:
            print("Failed to get sheets service")
            return None
            
        print("Getting spreadsheet...")
        sheet = service.spreadsheets()
        print(f"Reading from spreadsheet {SPREADSHEET_ID}")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        values = result.get('values', [])
        print(f"Successfully read {len(values)} rows from sheet")
        if values:
            print("First row (headers):", values[0])
        return values
    except Exception as e:
        print(f"\nError reading sheet: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {sys.exc_info()}")
        return None

def format_sheet_data_for_prompt(sheet_data):
    if not sheet_data:
        return "No data available in the sheet."
    
    try:
        # Assuming first row contains headers
        headers = sheet_data[0]
        data_rows = sheet_data[1:]
        
        # Format the data in a way that's easy for the AI to understand
        formatted_data = "Here is the data from our sheet:\n"
        for row in data_rows:
            row_dict = dict(zip(headers, row))
            formatted_data += f"- {', '.join(f'{k}: {v}' for k, v in row_dict.items())}\n"
        
        print("\nFormatted data for AI:", formatted_data)
        return formatted_data
    except Exception as e:
        print(f"Error formatting data: {str(e)}")
        return "Error formatting sheet data."

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            print(f"\nProcessing query: {user_query}")
            
            # First, ask the LLM if this query needs sheet data
            context_check_prompt = f"""You are a query classifier. Your task is to determine if a question requires specific data from our database to answer accurately.

            Rules for classification:
            1. If the question is about general knowledge, historical facts, scientific facts, or information that doesn't require specific data from our database, respond with 'NO_SHEET_DATA_NEEDED'
            2. If the question is about specific data that should be in our database (like population statistics, demographic data, financial records, or any specific records), respond with 'SHEET_DATA_NEEDED'
            3. If the question is about current statistics, demographics, or specific data points that would be stored in our database, respond with 'SHEET_DATA_NEEDED'
            4. If you're unsure, respond with 'NO_SHEET_DATA_NEEDED' to allow the AI to use its general knowledge

            Examples:
            - "What is the capital of France?" -> NO_SHEET_DATA_NEEDED
            - "How many females in Texas this year?" -> SHEET_DATA_NEEDED
            - "What is the population of New York?" -> SHEET_DATA_NEEDED
            - "Who was the first president of the United States?" -> NO_SHEET_DATA_NEEDED
            - "How many complete t rex skulls have been found?" -> NO_SHEET_DATA_NEEDED
            - "What is the current GDP of China?" -> SHEET_DATA_NEEDED
            - "What is the atomic number of gold?" -> NO_SHEET_DATA_NEEDED

            Question to classify: {user_query}
            
            Respond with ONLY 'SHEET_DATA_NEEDED' or 'NO_SHEET_DATA_NEEDED'."""
            
            context_check = generate_content_with_retry(model, context_check_prompt)
            needs_sheet_data = context_check.strip() == 'SHEET_DATA_NEEDED'
            
            print(f"Sheet data needed: {needs_sheet_data}")
            
            if needs_sheet_data:
                # Get sheet data only if needed
                sheet_data = read_sheet()
                if sheet_data is None:
                    ai_response = "I apologize, but I'm unable to access the database at the moment. Please try again later or ask a general knowledge question instead."
                else:
                    context = format_sheet_data_for_prompt(sheet_data)
                    prompt = f"{context}\n\nBased on this data, please answer the following question: {user_query}"
                    ai_response = generate_content_with_retry(model, prompt)
            else:
                # Answer directly without sheet data
                ai_response = generate_content_with_retry(model, user_query)
            
            print("\nAI Response:", ai_response)
        except Exception as e:
            print(f"\nError in chat route: {str(e)}")
            if "429" in str(e):
                ai_response = "I'm currently experiencing high demand. Please try again in a few moments."
            else:
                ai_response = f"I apologize, but I encountered an error. Please try again or rephrase your question."
        return render_template('index.html', user_query=user_query, ai_response=ai_response)
    else:
        return render_template('index.html', user_query=None, ai_response=None)

@app.route("/sheet", methods=['GET'])
def view_sheet():
    sheet_data = read_sheet()
    if sheet_data is None:
        return "Error reading sheet data", 500
    return render_template('sheet.html', data=sheet_data)

if __name__ == '__main__':
    app.run(debug=True)