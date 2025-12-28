# config.py
# Configuration variables for the backend.

import os

# Use absolute path based on this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_STORAGE_PATH = os.path.join(BASE_DIR, "received_files")

# Ensure the directory exists
os.makedirs(BASE_STORAGE_PATH, exist_ok=True)
