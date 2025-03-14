import os
import logging
from datetime import datetime
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

def log_status(message, level='info'):
    """Log a message and return it for UI display"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    
    if level == 'error':
        logger.error(log_msg)
    else:
        logger.info(log_msg)
    
    return message

# Gemini API Key (Load from environment variable)
GOOGLE_API_KEY = "AIzaSyBq7nlkEPVytgPdXYQ6hQUrN6pWuusoFsc"
status_messages = []
status_messages.append(log_status("Starting Koba AI Assistant..."))
status_messages.append(log_status(f"API Key configured: {GOOGLE_API_KEY[:10]}..."))

# Configure the Gemini API with explicit settings
try:
    genai.configure(
        api_key=GOOGLE_API_KEY,
        transport="rest",  # Force REST transport
        client_options={"api_endpoint": "generativelanguage.googleapis.com"}  # Explicit API endpoint
    )
    status_messages.append(log_status("Gemini API configured successfully"))
except Exception as e:
    status_messages.append(log_status(f"Error configuring Gemini API: {str(e)}", 'error'))

# Initialize model
model = None
try:
    status_messages.append(log_status("Initializing Gemini model..."))
    model = genai.GenerativeModel('gemini-pro')
    
    status_messages.append(log_status("Testing model connection..."))
    test_response = model.generate_content("test")
    status_messages.append(log_status("✓ Model initialized and tested successfully"))
except Exception as e:
    error_msg = f"Error initializing model: {str(e)}"
    status_messages.append(log_status(error_msg, 'error'))
    model = None

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_query = request.form['user_query']
        log_status(f"Received query: {user_query}")
        
        try:
            if model is None:
                error_msg = "AI model not initialized. Check logs for details."
                log_status(error_msg, 'error')
                return render_template('index.html', 
                    user_query=user_query,
                    ai_response=error_msg,
                    status_messages=status_messages)
            
            log_status("Generating response...")
            response = model.generate_content(user_query)
            ai_response = response.text
            log_status("Response generated successfully")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            log_status(error_msg, 'error')
            ai_response = error_msg
            
        return render_template('index.html', 
            user_query=user_query, 
            ai_response=ai_response,
            status_messages=status_messages)
    else:
        return render_template('index.html', 
            user_query=None, 
            ai_response=None,
            status_messages=status_messages)

# This is needed for Vercel
app.debug = False 