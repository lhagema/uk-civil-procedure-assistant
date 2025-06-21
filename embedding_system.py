"""
Embedding System for CPR Documents using Google's Text Embedding API

This module provides:
- Document embedding using Google's Text Embedding API
- Vector database storage using ChromaDB
- Semantic search functionality
- Document chunking and processing
"""

import os
import json
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import chromadb  # type: ignore
from chromadb.config import Settings  # type: ignore
import numpy as np  # type: ignore
from google import genai  # type: ignore
from google.genai.types import HttpOptions, EmbedContentConfig  # type: ignore

class CPREmbeddingSystem:
    """
    Embedding system for CPR documents using Google's Text Embedding API
    """
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.embedding_model = "gemini-embedding-001"  # New Vertex AI embedding model
        self.chunk_size = 1000  # Characters per chunk
        self.chunk_overlap = 200  # Overlap between chunks
        self.batch_size = 20  # Number of chunks to process in a single API call
        self.client = None
        self.chroma_client = None
        self.collection = None
        self.initialized = False
        
    def initialize(self):
        """Initialize Google Generative AI client and ChromaDB"""
        try:
            # Set environment variables for Vertex AI
            os.environ["GOOGLE_CLOUD_PROJECT"] = self.project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = self.location
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
            
            # Initialize Google Generative AI client
            self.client = genai.Client(http_options=HttpOptions(api_version="v1"))
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            try:
                self.collection = self.chroma_client.get_collection("cpr_documents")
                print("✅ Loaded existing CPR document embeddings")
            except:
                self.collection = self.chroma_client.create_collection("cpr_documents")
                print("✅ Created new CPR document embeddings collection")
            
            self.initialized = True
            print("✅ Embedding system initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize embedding system: {e}")
            self.initialized = False
    
    def chunk_text(self, text: str, filename: str) -> List[Dict]:
        """
        Split text into overlapping chunks for embedding
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + self.chunk_size * 0.7:  # Only break if we find a good sentence boundary
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "filename": filename,
                    "start": start,
                    "end": end
                })
            
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks
    
    def get_embedding(self, text: str, title: str = "") -> list:
        """Get embedding for text using Google's Vertex AI Gemini Embedding API"""
        try:
            config = EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=3072,
                title=title or None
            )
            response = self.client.models.embed_content(  # type: ignore
                model=self.embedding_model,
                contents=text,
                config=config
            )
            # The embedding is in response.embeddings[0].values
            return response.embeddings[0].values
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def batch_embed(self, texts: List[str], titles: Optional[List[str]] = None) -> List[List[float]]:
        """Get embeddings for multiple texts in a single API call"""
        if not texts:
            return []
        
        if titles is None:
            titles = []
        
        try:
            # Prepare contents for batch embedding
            contents = []
            for i, text in enumerate(texts):
                title = titles[i] if titles and i < len(titles) else ""
                contents.append({
                    "text": text,
                    "title": title or None
                })
            
            config = EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=3072
            )
            
            response = self.client.models.embed_content(  # type: ignore
                model=self.embedding_model,
                contents=contents,
                config=config
            )
            
            # Extract embeddings from response
            embeddings = []
            for embedding in response.embeddings:
                embeddings.append(embedding.values)
            
            return embeddings
            
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            return []
    
    def process_cpr_documents(self, cpr_data_dir: str = "cpr_data"):
        """Process and embed all CPR documents"""
        if not self.initialized:
            print("❌ Embedding system not initialized")
            return
        
        cpr_path = Path(cpr_data_dir)
        if not cpr_path.exists():
            print(f"❌ CPR data directory not found: {cpr_data_dir}")
            return
        
        # Get all markdown files
        md_files = list(cpr_path.glob("*.md"))
        print(f"📚 Found {len(md_files)} CPR documents to process")
        
        total_chunks = 0
        processed_files = 0
        
        for md_file in md_files:
            try:
                print(f"Processing: {md_file.name}")
                
                # Read the file
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip empty files
                if not content.strip():
                    continue
                
                # Chunk the content
                chunks = self.chunk_text(content, md_file.name)
                
                # Process chunks in batches
                all_embeddings = []
                all_texts = []
                all_metadatas = []
                all_ids = []
                
                for i in range(0, len(chunks), self.batch_size):
                    batch_chunks = chunks[i:i + self.batch_size]
                    batch_texts = [chunk["text"] for chunk in batch_chunks]
                    batch_titles = [chunk["filename"] for chunk in batch_chunks]
                    
                    # Get batch embeddings
                    batch_embeddings = self.batch_embed(batch_texts, batch_titles)
                    
                    # Process batch results
                    for j, (chunk, embedding) in enumerate(zip(batch_chunks, batch_embeddings)):
                        if embedding:
                            all_embeddings.append(embedding)
                            all_texts.append(chunk["text"])
                            all_metadatas.append({
                                "filename": chunk["filename"],
                                "start": chunk["start"],
                                "end": chunk["end"],
                                "chunk_index": i + j
                            })
                            all_ids.append(f"{md_file.stem}_{i + j}")
                    
                    # Progress indicator for large files
                    if len(chunks) > 20:
                        print(f"  Processed batch {i//self.batch_size + 1}/{(len(chunks) + self.batch_size - 1)//self.batch_size}")
                
                # Add to collection
                if all_embeddings:
                    self.collection.add(  # type: ignore
                        embeddings=all_embeddings,
                        documents=all_texts,
                        metadatas=all_metadatas,
                        ids=all_ids
                    )
                    total_chunks += len(all_embeddings)
                    processed_files += 1
                    print(f"  ✅ Added {len(all_embeddings)} chunks")
                
            except Exception as e:
                print(f"  ❌ Error processing {md_file.name}: {e}")
        
        print(f"✅ Processing complete: {processed_files} files, {total_chunks} chunks embedded")
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents using semantic similarity
        """
        if not self.initialized or not self.collection:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            if not query_embedding:
                return []
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    formatted_results.append({
                        "text": doc,
                        "filename": metadata["filename"],
                        "relevance_score": 1 - distance,  # Convert distance to similarity score
                        "metadata": metadata
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def get_document_context(self, query: str, max_chars: int = 3000) -> str:
        """
        Get relevant document context for a query
        """
        results = self.search_documents(query, top_k=3)
        
        if not results:
            return ""
        
        # Combine relevant chunks
        context_parts = []
        current_length = 0
        
        for result in results:
            if current_length + len(result["text"]) > max_chars:
                break
            
            context_parts.append(f"From {result['filename']}:\n{result['text']}\n")
            current_length += len(result["text"])
        
        return "\n".join(context_parts)

def setup_embedding_environment():
    """Setup environment for embedding system"""
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("⚠️  Missing GCP environment variable:")
        print("   - GOOGLE_CLOUD_PROJECT")
        print("\nTo enable embedding features:")
        print("1. Set GOOGLE_CLOUD_PROJECT to your project ID")
        print("2. Run: gcloud auth application-default login")
        print("3. Make sure you have enabled Vertex AI API in your GCP project")
        return False
    return True

# Global embedding system instance
embedding_system = None

def initialize_embedding_system():
    """Initialize the global embedding system"""
    global embedding_system
    
    if not setup_embedding_environment():
        return False
    
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            print("❌ GOOGLE_CLOUD_PROJECT environment variable not set.")
            return False
        embedding_system = CPREmbeddingSystem(project_id)
        embedding_system.initialize()
        return embedding_system.initialized
    except Exception as e:
        print(f"Failed to initialize embedding system: {e}")
        return False

def get_relevant_context(query: str) -> str:
    """Get relevant context for a query using embeddings"""
    global embedding_system
    
    if not embedding_system or not embedding_system.initialized:
        return ""
    
    return embedding_system.get_document_context(query) 