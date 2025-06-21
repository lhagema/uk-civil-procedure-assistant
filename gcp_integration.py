"""
GCP Vertex AI Integration for Legal AI Assistant

This module provides integration with Google Cloud Platform services:
- Vertex AI for text generation using Google Generative AI SDK
- Enhanced legal query processing with LLM capabilities
"""

import os
from typing import List, Dict, Optional
from embedding_system import initialize_embedding_system, get_relevant_context

class GCPLegalAssistant:
    """
    Enhanced legal assistant using GCP Vertex AI services (Google Generative AI SDK)
    """
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.initialized = False
        self.client = None
        # Initialize embedding system
        self.embedding_ready = initialize_embedding_system()
        
    def initialize(self):
        """Initialize Google Generative AI client with Vertex AI"""
        try:
            import os
            from google import genai
            os.environ["GOOGLE_CLOUD_PROJECT"] = self.project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = self.location
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
            self.client = genai.Client()
            self.initialized = True
            print("✅ Google Generative AI SDK initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Google Generative AI SDK: {e}")
            self.initialized = False
    
    def generate_legal_response(self, query: str, context: str = "") -> str:
        """Generate legal response using Google Generative AI SDK, with embedding context if available"""
        if not self.initialized or not self.client:
            return "GCP services not available. Please check your configuration."
        try:
            from google import genai
            # Get relevant context from embeddings
            embedding_context = get_relevant_context(query) if self.embedding_ready else ""
            prompt = f"""
You are a legal AI assistant specializing in UK Civil Procedure Rules (CPR). 
Please provide a helpful, accurate response to the following legal query.

Relevant CPR context:
{embedding_context}

User Query: {query}

For procedural questions, structure your response in the following format:

## Key Points
• [1-3 most important points only, use 3 only if necessary]

## Practical Steps
[Provide concise step-by-step guidance including:
- Forms to use (if applicable)
- Where to file
- Key requirements]

## Important Deadlines/Time Limits
[Highlight any critical time limits or deadlines]

## Relevant CPR Rules
[Cite specific CPR rules with their numbers and brief descriptions]

## Additional Considerations
[Any other important points or warnings]

For non-procedural questions, provide a clear, well-structured response that directly addresses the query.

Keep your response:
- Clear and well-structured
- Practical for legal practitioners
- Accurate to UK Civil Procedure Rules
- Focused and concise
- Professional in tone

Use the relevant CPR context provided above to inform your response."""
            # Generate response using the SDK
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Sorry, I encountered an error while processing your query: {str(e)}"

def setup_gcp_environment():
    """Setup GCP environment variables and authentication"""
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("⚠️  Missing GCP environment variable:")
        print("   - GOOGLE_CLOUD_PROJECT")
        print("\nTo enable GCP features:")
        print("1. Set GOOGLE_CLOUD_PROJECT to your project ID")
        print("2. Run: gcloud auth application-default login")
        print("3. Make sure you have enabled Vertex AI API in your GCP project")
        return False
    return True

def enhanced_legal_query(query: str) -> Dict:
    """Enhanced legal query using GCP Vertex AI"""
    if not setup_gcp_environment():
        return {
            "success": False,
            "answer": "GCP not configured. Please set up your Google Cloud credentials.",
            "citations": [],
            "query": query
        }
    
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            return {
                "success": False,
                "answer": "GOOGLE_CLOUD_PROJECT environment variable not set.",
                "citations": [],
                "query": query
            }
            
        assistant = GCPLegalAssistant(project_id)
        assistant.initialize()
        
        response = assistant.generate_legal_response(query)
        
        return {
            "success": True,
            "answer": response,
            "citations": [],  # LLM will include citations in the text
            "query": query
        }
        
    except Exception as e:
        return {
            "success": False,
            "answer": f"Error processing query: {str(e)}",
            "citations": [],
            "query": query
        } 