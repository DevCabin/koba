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

# List available models and initialize
try:
    available_models = genai.list_models()
    print("Available models:", [model.name for model in available_models])
    
    # Try to find a suitable model
    model_names = ['gemini-pro', 'gemini-1.5-pro', 'models/gemini-pro', 'models/gemini-1.5-pro']
    model = None
    
    for model_name in model_names:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            # Test the model
            test_response = model.generate_content("test")
            print(f"Successfully initialized model: {model_name}")
            break
        except Exception as e:
            print(f"Failed to initialize {model_name}: {str(e)}")
            continue
            
    if model is None:
        print("Failed to initialize any model")
        raise RuntimeError("No working model found")
        
except Exception as e:
    print(f"Error during initialization: {str(e)}")
    model = None

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        try:
            if model is None:
                return render_template('index.html', 
                    user_query=user_query, 
                    ai_response="System initialization failed. Please check server logs.")
            
            response = model.generate_content(user_query)
            ai_response = response.text
        except Exception as e:
            ai_response = f"Error: {str(e)}"
        return render_template('index.html', user_query=user_query, ai_response=ai_response)
    else:
        return render_template('index.html', user_query=None, ai_response=None)

# This is needed for Vercel
app.debug = False 