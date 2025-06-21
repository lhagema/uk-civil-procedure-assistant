"""
Configuration file for GCP settings
Edit this file with your actual GCP project details
"""

import os

# GCP Configuration
# Replace this with your actual project ID
GCP_PROJECT_ID = "hack-thelaw25cam-577"  # Your project ID here

# Set environment variable if not already set
if not os.getenv("GOOGLE_CLOUD_PROJECT"):
    os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT_ID

# No service account needed! We'll use Application Default Credentials
# This means you just need to run: gcloud auth application-default login

# Example configuration (uncomment and modify):
# GCP_PROJECT_ID = "my-legal-ai-project-123456"
# GCP_CREDENTIALS_PATH = "/Users/lauramariehagemann/Downloads/my-service-account-key.json" 