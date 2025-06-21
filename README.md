# Legal AI Assistant

A FastAPI-based legal assistant that provides information about UK Civil Procedure Rules (CPR) using both keyword matching and Google Cloud Vertex AI integration.

## Features

- **LLM Integration**: Uses Google Cloud Vertex AI (PaLM 2) for intelligent legal responses
- **Fallback System**: Keyword-based matching when GCP is not configured
- **Web Interface**: Clean HTML interface for querying legal information
- **API Endpoints**: RESTful API for programmatic access

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. GCP Configuration (Optional but Recommended)

To enable LLM capabilities, you need to set up Google Cloud Platform:

1. **Create a GCP Project** (if you don't have one)
2. **Enable Vertex AI API** in your GCP project
3. **Create a Service Account** with Vertex AI permissions
4. **Download the service account key** as a JSON file
5. **Set Environment Variables**:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

### 3. Run the Application

```bash
python main.py
```

Or for development with auto-reload:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## How It Works

### With GCP Integration (Recommended)
- Queries are processed by Google Cloud's PaLM 2 model
- The LLM provides intelligent, contextual responses about UK CPR
- Responses include relevant rule citations and practical guidance

### Without GCP (Fallback)
- Uses keyword-based matching against a predefined knowledge base
- Covers common topics like witness statements, track allocation, etc.
- Limited to predefined responses but still functional

## API Usage

### Query Endpoint
```
POST /api/query
Content-Type: application/x-www-form-urlencoded

query=your legal question here
```

### Response Format
```json
{
  "success": true,
  "answer": "Detailed legal response...",
  "citations": ["CPR 32.4(1)", "CPR 32.10"],
  "query": "original query"
}
```

## Current Knowledge Base (Fallback Mode)

The fallback system covers:
- Witness statements and exchange procedures
- Track allocation (small claims, fast track, multi-track)
- Particulars of claim deadlines
- Strike out applications

## Development

The application is built with:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Jinja2**: Template engine
- **Google Cloud AI Platform**: LLM integration

## Troubleshooting

### GCP Issues
- Ensure Vertex AI API is enabled
- Check service account permissions
- Verify environment variables are set correctly

### Fallback Mode
If GCP is not configured, the app will automatically use the keyword-based system and display a warning message.

## License

This project is for demonstration purposes. The Civil Procedure Rules and Practice Directions are available under the Open Government Licence.

## Contributing

This is a hackathon MVP. For production use, consider:
- Implementing proper authentication
- Adding comprehensive error handling
- Integrating with official legal databases
- Adding comprehensive testing 