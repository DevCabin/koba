import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gemini API Key (Load from environment variable)
GOOGLE_API_KEY = "AIzaSyBq7nlkEPVytgPdXYQ6hQUrN6pWuusoFsc"  # Direct key for testing
print(f"API Key being used: {GOOGLE_API_KEY}")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            print(f"Attempting to generate content with query: {user_query}")
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