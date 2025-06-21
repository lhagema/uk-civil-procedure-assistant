# Legal AI Assistant - Civil Procedure Navigator

A fast, modern MVP for navigating Civil Procedure Rules using AI assistance. This prototype demonstrates how AI can transform static legal rules into dynamic, personalized guidance.

## Features

- **Fast, Modern UI**: Beautiful, responsive chat interface built with FastAPI and vanilla JavaScript
- **Legal Knowledge Base**: Pre-loaded with key Civil Procedure Rules and Practice Directions
- **Citation Support**: Automatic citation of relevant CPR rules and practice directions
- **Example Questions**: Quick-start buttons for common procedural questions
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and setup environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```

3. **Open your browser:**
Navigate to `http://localhost:8000`

## Usage

The application provides a chat interface where you can ask questions about civil procedure, such as:

- "When do witness statements need to be exchanged?"
- "How does the court allocate cases to a track?"
- "What are the time limits for serving particulars of claim?"
- "How do I make an application to strike out a statement of case?"

## Current Knowledge Base

The MVP includes information on:
- **Witness Statements**: Timing, exchange procedures, and consequences
- **Track Allocation**: Small claims, fast track, intermediate track, and multi-track
- **Particulars of Claim**: Service deadlines and extension procedures
- **Strike Out Applications**: Grounds, procedures, and evidence requirements

## Architecture

- **Backend**: FastAPI with async support for high performance
- **Frontend**: Modern HTML/CSS/JavaScript with responsive design
- **Knowledge Base**: Structured data with citations (easily expandable)
- **API**: RESTful endpoints for query processing

## Future Enhancements

This MVP is designed to be easily enhanced with:

1. **GCP Vertex AI Integration**: 
   - Embeddings for semantic search
   - Large language models for more sophisticated responses
   - Vector database for full CPR/PD search

2. **Advanced Features**:
   - Follow-up question handling
   - Visual flowcharts and timelines
   - Direct links to official forms
   - Multi-topic support

3. **Deployment**:
   - Cloud Run for serverless deployment
   - Cloud Storage for document storage
   - Cloud SQL for persistent data

## Development

### Project Structure
```
├── main.py              # FastAPI application
├── templates/
│   └── index.html       # Frontend template
├── static/              # Static assets (if needed)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Knowledge

To add new legal topics, edit the `LEGAL_KNOWLEDGE` dictionary in `main.py`:

```python
LEGAL_KNOWLEDGE = {
    "your_topic": {
        "answer": "Your detailed answer here...",
        "citations": ["CPR X.Y", "Practice Direction X"]
    }
}
```

## License

This project is for demonstration purposes. The Civil Procedure Rules and Practice Directions are available under the Open Government Licence.

## Contributing

This is a hackathon MVP. For production use, consider:
- Implementing proper authentication
- Adding comprehensive error handling
- Integrating with official legal databases
- Adding comprehensive testing 