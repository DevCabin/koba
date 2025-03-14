import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gemini API Key (Load from environment variable)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
print(f"API Key loaded: {GOOGLE_API_KEY[:10]}..." if GOOGLE_API_KEY else "No API key found")

if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            print(f"Using API key: {GOOGLE_API_KEY[:10]}...")  # Debug log
            response = model.generate_content(user_query)
            ai_response = response.text
        except Exception as e:
            print(f"Error details: {str(e)}")  # Debug log
            ai_response = f"Error: {str(e)}"
        return render_template('index.html', user_query=user_query, ai_response=ai_response)
    else:
        return render_template('index.html', user_query=None, ai_response=None)

# This is needed for Vercel
app.debug = False

# Remove the if __name__ == '__main__' block as it's not needed for serverless 