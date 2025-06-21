"""
Script to embed all CPR documents using Google's Text Embedding API and ChromaDB.
Run this script after adding new CPR documents or updating existing ones.
"""

import embedding_system

if __name__ == "__main__":
    print("Initializing embedding system...")
    if embedding_system.initialize_embedding_system():
        print("Processing CPR documents for embedding...")
        embedding_system.embedding_system.process_cpr_documents("cpr_data")
        print("✅ All CPR documents embedded!")
    else:
        print("❌ Failed to initialize embedding system. Check your GCP credentials and environment variables.") 