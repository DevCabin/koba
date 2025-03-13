# Koba - AI Chat Interface with Google Sheets Integration

Version 1.2 - Stable Release

## Current Features

- **Dual-Mode AI Assistant**
  - General knowledge queries using Gemini 1.5 Pro
  - Data-driven responses using Google Sheets integration
  - Automatic (configurable) query classification to determine query routing needs

- **Google Sheets Integration**
  - Secure OAuth2 authentication
  - Automatic sheet data reading and formatting
  - Dynamic sheet name detection
  - Error handling and retry logic

- **Robust Error Handling**
  - Rate limit management with exponential backoff
  - Graceful fallbacks for API failures
  - Detailed error logging

- **User Interface**
  - Clean, responsive web interface
  - Real-time query processing
  - Clear response formatting

## Technical Stack

- Python 3.x
- Flask (Web Framework)
- Google Generative AI (Gemini 1.5 Pro)
- Google Sheets API
- OAuth2 Authentication

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   SPREADSHEET_ID=your_google_sheet_id
   ```
4. Place your `credentials.json` file in the project root
5. Run the application:
   ```bash
   python chat.py
   ```
6. Access the application at `http://127.0.0.1:5001`

## TODO List

### High Priority
- [ ] Add conversation memory/context
  - Implement chat history storage
  - Enable follow-up questions
  - Maintain context across queries
  - Add conversation export functionality

- [ ] Enhance UI/UX
  - Implement a modern chat interface
  - Add typing indicators
  - Support markdown formatting in responses
  - Add dark/light mode toggle
  - Implement responsive design for mobile

### Medium Priority
- [ ] Add data visualization
  - Create charts for sheet data
  - Add interactive data tables
  - Implement data filtering options

- [ ] Improve error handling
  - Add user-friendly error messages
  - Implement automatic recovery procedures
  - Add detailed error reporting

### Low Priority
- [ ] Add multi-sheet support
  - Enable querying across multiple sheets
  - Add sheet selection interface
  - Implement sheet relationship mapping

- [ ] Add export functionality
  - Export conversations to PDF/CSV
  - Save chat history
  - Share conversations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Hit me up @ devcabin.com

## License

This project is licensed under the MIT License - see the LICENSE file for details. 