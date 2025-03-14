import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gemini API Key (Load from environment variable)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# List available models to ensure we're using a valid one
try:
    models = genai.list_models()
    model = genai.GenerativeModel('gemini-1.5-pro-001')  # Using the latest stable version
except Exception as e:
    # Fallback to gemini-pro if 1.5 is not available
    model = genai.GenerativeModel('gemini-pro')

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            response = model.generate_content(user_query)
            ai_response = response.text
        except Exception as e:
            ai_response = f"Error communicating with Gemini: {str(e)}"
        return render_template('index.html', user_query=user_query, ai_response=ai_response)
    else:
        return render_template('index.html', user_query=None, ai_response=None)

# This is needed for Vercel
app.debug = False

# Remove the if __name__ == '__main__' block as it's not needed for serverless 