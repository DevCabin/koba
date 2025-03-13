# Koba - AI Chat Interface with Google Sheets Integration

Version 1.2 - Stable Release

## Current Features

- **Dual-Mode AI Assistant**
  - General knowledge queries using Gemini 1.5 Pro
  - Data-driven responses using Google Sheets integration
  - Automatic query classification to determine data needs

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

## Development Roadmap

### Phase 1: Modern UI/UX Enhancement
#### Visual Design System
- Implement a modern color palette with gradients
- Create a dark/light mode system
- Design a consistent typography system
- Establish spacing and layout guidelines

#### Interactive Elements
- Add gradient shimmer effects on interactive elements
- Implement smooth transitions and animations
- Create a particle system background using Three.js or Particles.js
- Design custom loading states and thinking animations

#### Chat Interface Modernization
- Implement a modern chat bubble design
- Add typing indicators with custom animations
- Create message transition effects
- Design a floating action button for new conversations

#### Technical Implementation
- Set up Tailwind CSS for utility-first styling
- Integrate GSAP for advanced animations
- Add Three.js for 3D particle effects
- Implement CSS variables for theming
- Optimize asset delivery and performance

### Phase 2: Conversational Memory & Context
#### Backend Implementation
- Set up PostgreSQL for conversation storage
- Design conversation schema
- Implement user session management
- Create conversation context tracking
- Implement conversation threading
- Add context window management
- Create conversation summarization
- Implement context pruning

#### Frontend Implementation
- Design conversation thread view
- Add conversation navigation
- Implement context indicators
- Create conversation grouping
- Add conversation branching
- Implement context switching
- Create conversation search
- Add conversation export

### Phase 3: Advanced Features
#### Data Visualization
- Implement Chart.js or D3.js
- Create interactive data tables
- Add data filtering system
- Implement real-time updates

#### Multi-sheet Support
- Add sheet selection interface
- Implement cross-sheet queries
- Create sheet relationship mapping
- Add sheet comparison views

#### Export & Sharing
- Implement PDF export
- Add CSV export
- Create conversation sharing
- Add API endpoints
- Implement conversation templates
- Add custom query presets
- Create user preferences
- Add keyboard shortcuts

### Phase 4: Polish & Optimization
#### Performance
- Implement caching system
- Add request batching
- Optimize database queries
- Add performance monitoring

#### Error Handling
- Implement comprehensive error states
- Add recovery procedures
- Create user feedback system
- Implement logging system

#### Documentation & Testing
- Create API documentation
- Add user guides
- Create developer documentation
- Add deployment guides
- Implement unit tests
- Add integration tests
- Create end-to-end tests
- Add performance tests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 