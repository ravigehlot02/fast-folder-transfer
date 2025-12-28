# safe_path.py
# Prevents unsafe paths like ../../etc/passwd
# Ensures user-defined paths always remain inside BASE_STORAGE_PATH

import os

def safe_join(base_dir, user_path):
    """
    Safely joins a user-specified path with the base directory.
    Prevents directory traversal by normalizing & checking path.
    """
    # Normalize both paths to absolute paths for comparison
    base_dir = os.path.abspath(base_dir)
    normalized = os.path.normpath(user_path).lstrip(os.sep)
    final_path = os.path.join(base_dir, normalized)
    final_path = os.path.abspath(final_path)

    # Check if final path is within base directory
    if not final_path.startswith(base_dir):
        raise ValueError("Invalid path: directory traversal detected")

    return final_path
