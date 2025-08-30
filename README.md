# Enhanced Personal Chatbot Application

## Overview
An advanced AI-powered personal chatbot for Denver Magtibay featuring enhanced document processing, analytics, and professional UI/UX.

**🚀 Live Demo:** Coming soon on Streamlit Cloud  
**👨‍💻 Developer:** [Denver Magtibay](https://github.com/WarDen-Git)  
**📧 Contact:** denver.am23onl009@spjain.org

## Features

### Phase 1 (Current)
- ✅ Enhanced document processing system
- ✅ Professional UI/UX with custom theming
- ✅ Visitor analytics dashboard
- ✅ Smart contact management system

### Phase 2 (Future)
- 🔄 Context-aware AI responses
- 🔄 Calendar integration
- 🔄 Multi-modal capabilities
- 🔄 Advanced tool integrations

## Project Structure
```
enhanced_chatbot/
├── src/
│   ├── components/          # Reusable UI components
│   ├── utils/              # Utility functions
│   └── database/           # Database models and operations
├── data/
│   ├── documents/          # Profile documents and files
│   └── analytics/          # Analytics and logs
├── static/                 # CSS, JS, images
├── templates/              # HTML templates
├── app.py                  # Main application
└── requirements.txt        # Dependencies
```

## Installation

### Quick Start
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key (required)
   - Add Pushover credentials (optional)

3. **Run the application:**
   ```bash
   python run.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   Open your browser to http://localhost:8501

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for notifications)
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
```

## Technologies Used
- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with FastAPI components
- **Database**: SQLite for analytics and contact management
- **AI**: OpenAI GPT models with function calling
- **Document Processing**: PyPDF2, python-docx, markdown
- **Analytics**: Plotly for visualizations