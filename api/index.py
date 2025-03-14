import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gemini API Key (Load from environment variable)
GOOGLE_API_KEY = "AIzaSyBq7nlkEPVytgPdXYQ6hQUrN6pWuusoFsc"
print(f"API Key being used: {GOOGLE_API_KEY}")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# List of model versions to try, from newest to oldest
MODEL_VERSIONS = [
    'gemini-1.5-pro',
    'gemini-1.0-pro',
    'gemini-pro'
]

# Try to initialize the model with fallback
model = None
last_error = None

for version in MODEL_VERSIONS:
    try:
        print(f"Attempting to initialize model version: {version}")
        model = genai.GenerativeModel(version)
        # Test the model with a simple query
        response = model.generate_content("test")
        print(f"Successfully initialized model version: {version}")
        break
    except Exception as e:
        print(f"Failed to initialize {version}: {str(e)}")
        last_error = e
        continue

if model is None:
    print(f"Failed to initialize any model version. Last error: {str(last_error)}")

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            if model is None:
                return render_template('index.html', 
                    user_query=user_query, 
                    ai_response="Error: No available model could be initialized. Please try again later.")
            
            print(f"Generating response for query: {user_query}")
            response = model.generate_content(user_query)
            ai_response = response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            ai_response = f"Error: {str(e)}"
        return render_template('index.html', user_query=user_query, ai_response=ai_response)
    else:
        return render_template('index.html', user_query=None, ai_response=None)

# This is needed for Vercel
app.debug = False

# Remove the if __name__ == '__main__' block as it's not needed for serverless 