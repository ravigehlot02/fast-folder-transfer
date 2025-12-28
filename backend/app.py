from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.responses import JSONResponse
from config import BASE_STORAGE_PATH
from utils.safe_path import safe_join
import hashlib

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Get absolute paths for frontend files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# Serve static files (CSS, JS)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/upload_folder")
async def upload_folder(
    files: list[UploadFile] = File(...),
    relativePaths: list[str] = Form(...)
):
    if len(files) != len(relativePaths):
        return JSONResponse({"error": "Files and paths mismatch"}, status_code=400)

    if not relativePaths:
        return JSONResponse({"error": "No files provided"}, status_code=400)

    # Get folder name from first file
    folder_name = relativePaths[0].split("/")[0]
    
    try:
        # Use safe_join to prevent directory traversal
        target_root = safe_join(BASE_STORAGE_PATH, folder_name)
        os.makedirs(target_root, exist_ok=True)

        uploaded_files = []
        for file, rel_path in zip(files, relativePaths):
            # Use safe_join for each file path
            safe_path = safe_join(BASE_STORAGE_PATH, rel_path.replace("/", os.sep))
            dir_path = os.path.dirname(safe_path)
            os.makedirs(dir_path, exist_ok=True)
            
            # Write file asynchronously
            with open(safe_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            uploaded_files.append(rel_path)

        return {"status": "success", "target_path": target_root, "uploaded_files": uploaded_files}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Upload failed: {str(e)}"}, status_code=500)

@app.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    relativePath: str = Form(...),
    folderName: str = Form(...)
):
    """Upload a single file - used for resumable uploads"""
    try:
        # Use safe_join to prevent directory traversal
        safe_path = safe_join(BASE_STORAGE_PATH, relativePath.replace("/", os.sep))
        dir_path = os.path.dirname(safe_path)
        
        # Ensure directory exists
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Write file
        with open(safe_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Verify file was written
        file_exists = os.path.exists(safe_path)
        file_size = os.path.getsize(safe_path) if file_exists else 0
        
        return {
            "status": "success", 
            "file_path": relativePath, 
            "saved_path": str(safe_path), 
            "storage_path": str(BASE_STORAGE_PATH),
            "file_exists": file_exists,
            "file_size": file_size
        }
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Upload failed: {str(e)}"}, status_code=500)

@app.get("/check_file/{folder_name:path}")
async def check_file(folder_name: str, file_path: str):
    """Check if a file exists and get its size"""
    try:
        safe_path = safe_join(BASE_STORAGE_PATH, file_path.replace("/", os.sep))
        if os.path.exists(safe_path):
            size = os.path.getsize(safe_path)
            return {"exists": True, "size": size}
        return {"exists": False, "size": 0}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Check failed: {str(e)}"}, status_code=500)

@app.get("/list_uploaded")
async def list_uploaded(folder_name: str):
    """List all uploaded files in a folder"""
    try:
        folder_path = safe_join(BASE_STORAGE_PATH, folder_name)
        if not os.path.exists(folder_path):
            return {"uploaded_files": [], "storage_path": str(BASE_STORAGE_PATH)}
        
        uploaded_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_STORAGE_PATH)
                uploaded_files.append(rel_path.replace(os.sep, "/"))
        
        return {"uploaded_files": uploaded_files, "storage_path": str(BASE_STORAGE_PATH), "folder_path": str(folder_path)}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"List failed: {str(e)}"}, status_code=500)

@app.get("/get_storage_path")
async def get_storage_path():
    """Get the storage path where files are saved"""
    return {"storage_path": str(BASE_STORAGE_PATH)}
