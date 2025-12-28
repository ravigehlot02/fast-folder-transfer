# Fast Folder Transfer

Fast Folder Transfer is a lightweight, user-friendly tool for transferring files and entire folder structures between devices on the same network. It features a modern web interface with real-time progress tracking, pause/resume capabilities, and robust error handling.

---

## Features

### Core Functionality
- **Simple Web UI** - Clean, intuitive interface accessible from any device on your network
- **Folder Structure Preservation** - Maintains complete folder hierarchies during transfer
- **Real-time Progress Tracking** - Individual progress bars for each file with upload status
- **Pause & Resume** - Pause uploads at any time and resume from where you left off
- **Add Files During Upload** - Select and add more files while uploads are in progress
- **Remove Files** - Remove files from the upload queue, even during active uploads
- **Automatic Resume** - Detects already uploaded files and skips them automatically
- **Safe Path Handling** - Prevents directory traversal attacks with path validation
- **Network Access** - Access from any device on your local network

### User Experience
- **Visual Status Indicators** - Color-coded file status (completed, uploading, paused, failed)
- **File Size Display** - Shows file sizes and upload progress in human-readable format
- **Error Handling** - Clear error messages and automatic retry capability
- **Storage Location Display** - Shows exact path where files are saved after completion

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows (tested on Windows 10/11)

### Setup

1. **Clone or download the repository**
   ```bash
   cd fast-folder-transfer
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Quick Start (Windows)

Simply run the provided batch file:
```bash
run_windows.bat
```

This will:
- Create/activate virtual environment
- Install dependencies
- Start the server on `http://localhost:8000`
- Open the web interface in your browser

### Manual Start

1. **Start the server**
   ```bash
   cd backend
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

2. **Access the interface**
   - Local: Open `http://localhost:8000` in your browser
   - Network: Access from other devices using `http://[YOUR_IP]:8000`
     - Find your IP: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)

### Using the Interface

1. **Select Folder**
   - Click "Select folder to transfer"
   - Choose a folder from your device
   - View file count and total size

2. **Start Transfer**
   - Click "Start Transfer" button
   - Watch real-time progress for each file
   - Green progress bars show upload status

3. **Manage Uploads**
   - **Pause**: Click "Pause" to temporarily stop uploads
   - **Resume**: Click "Resume" to continue from where you paused
   - **Remove Files**: Click "Remove" next to any file to exclude it from upload
   - **Add More Files**: Select additional folders/files while upload is in progress

4. **Completion**
   - Success message shows the exact storage location
   - Files are saved to `backend/received_files/[folder_name]/`

---

## Project Structure

```
fast-folder-transfer/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── config.py              # Configuration (storage paths)
│   ├── requirements.txt        # Python dependencies
│   ├── received_files/         # Default storage location for uploaded files
│   └── utils/
│       ├── safe_path.py        # Path validation and security
│       ├── file_writer.py      # File writing utilities
│       └── background_worker.py  # Background task processing
├── frontend/
│   ├── index.html             # Main web interface
│   └── assets/
│       └── style.css          # Styling
├── run_windows.bat            # Windows launcher script
└── README.md                  # This file
```

---

## API Endpoints

### Frontend Routes
- `GET /` - Serves the main web interface
- `GET /assets/*` - Static assets (CSS, JS)

### Backend API
- `POST /upload_folder` - Upload multiple files with folder structure (legacy)
- `POST /upload_file` - Upload a single file (used for resumable uploads)
- `GET /list_uploaded` - List all uploaded files in a folder
- `GET /get_storage_path` - Get the storage directory path
- `GET /check_file` - Check if a specific file exists

---

## Configuration

### Storage Location

Files are saved to `backend/received_files/` by default. To change this:

1. Edit `backend/config.py`
2. Modify `BASE_STORAGE_PATH`:
   ```python
   BASE_STORAGE_PATH = os.path.join(BASE_DIR, "your_custom_folder")
   ```

### Server Settings

Default server settings:
- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `8000`

To change port, modify `run_windows.bat` or start manually:
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

---

## Features in Detail

### Progress Tracking
- Individual progress bars for each file
- Real-time percentage and size information
- Visual status indicators (green = completed, orange = paused, red = failed)

### Pause/Resume
- Pause uploads at any time
- Resume from the exact point where you paused
- Already uploaded files are automatically skipped

### File Management
- Remove files from queue before or during upload
- Add new files while upload is in progress
- Automatic duplicate detection

### Security
- Path validation prevents directory traversal attacks
- All file paths are sanitized and validated
- Files are restricted to the designated storage directory

---

## Troubleshooting

### Files Not Appearing
- Check `backend/received_files/` directory
- Verify server has write permissions
- Check browser console for errors

### Network Access Issues
- Ensure firewall allows port 8000
- Verify devices are on the same network
- Use `0.0.0.0` as host (not `localhost`)

### Upload Failures
- Check network connection
- Verify sufficient disk space
- Review error messages in the interface

### Port Already in Use
- Change port in `run_windows.bat` or command line
- Or stop the process using port 8000

---

## Technical Details

### Dependencies
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Python-multipart** - File upload handling
- **aiofiles** - Async file operations

### Browser Compatibility
- Chrome/Edge (recommended)
- Firefox
- Safari
- Any modern browser with JavaScript enabled

### Network Requirements
- Devices must be on the same local network
- No internet connection required
- Works with WiFi and Ethernet

---

## Development

### Running in Development Mode
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Project Architecture
- **Backend**: FastAPI with async file handling
- **Frontend**: Vanilla JavaScript with XMLHttpRequest for progress tracking
- **Storage**: Local file system with organized folder structure

---

## License

See LICENSE file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## Support

For issues, questions, or contributions, please open an issue on the repository.
