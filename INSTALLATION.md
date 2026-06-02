# QR Code Generator - Installation & Setup Guide

Complete step-by-step guide to install and run the QR Code Generator application.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 100 MB disk space
- 512 MB RAM
- Internet connection (for pip dependencies)

### Supported Operating Systems
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, Debian, CentOS)

### Required Software
- Python 3.8+
- pip (comes with Python)

---

## Windows Installation

### Step 1: Install Python
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Choose "Install Now" or customize installation
5. Complete installation

### Step 2: Verify Python Installation
Open Command Prompt and run:
```bash
python --version
pip --version
```

You should see version numbers (e.g., Python 3.10.0, pip 21.0.1)

### Step 3: Download Project Files
1. Download the QR Generator project
2. Extract to desired location (e.g., C:\Users\YourName\Desktop\QR)

### Step 4: Open Command Prompt in Project Folder
```bash
# Navigate to project directory
cd C:\Users\YourName\Desktop\QR\qr_generator

# Verify you're in correct folder
dir  # Should see app.py, requirements.txt, etc.
```

### Step 5: Create Virtual Environment
```bash
python -m venv venv
```

**What this does**: Creates an isolated Python environment for the project.

### Step 6: Activate Virtual Environment
```bash
# For Command Prompt:
.\venv\Scripts\activate

# For PowerShell:
.\venv\Scripts\Activate.ps1

# For Git Bash:
source venv/Scripts/activate
```

You should see `(venv)` prefix in your terminal.

**Note**: If PowerShell shows execution policy error:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 7: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs Flask, SQLAlchemy, and all other required packages.

### Step 8: Create Necessary Folders
```bash
mkdir static\uploads
mkdir static\generated_qr
```

### Step 9: Run the Application (Quick Method)
Double-click `run.bat` file in the project folder.

### Step 10: Alternative - Manual Run
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py
```

### Step 11: Access the Application
Open browser and go to: **http://localhost:5000**

---

## macOS Installation

### Step 1: Install Python
Using Homebrew (recommended):
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

Or download from https://www.python.org/downloads/macos/

### Step 2: Verify Installation
```bash
python3 --version
pip3 --version
```

### Step 3: Navigate to Project
```bash
cd ~/Desktop/QR/qr_generator
```

### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 5: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in terminal.

### Step 6: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 7: Create Necessary Folders
```bash
mkdir -p static/uploads
mkdir -p static/generated_qr
```

### Step 8: Make Run Script Executable
```bash
chmod +x run.sh
```

### Step 9: Run the Application (Quick Method)
```bash
./run.sh
```

### Step 10: Alternative - Manual Run
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```

### Step 11: Access the Application
Open Safari or Chrome: **http://localhost:5000**

---

## Linux Installation

### Step 1: Install Python and pip
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### Step 2: Verify Installation
```bash
python3 --version
pip3 --version
```

### Step 3: Navigate to Project
```bash
cd ~/Desktop/QR/qr_generator
# Or wherever you extracted the files
```

### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 5: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in terminal.

### Step 6: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 7: Create Necessary Folders
```bash
mkdir -p static/uploads
mkdir -p static/generated_qr
```

### Step 8: Make Run Script Executable
```bash
chmod +x run.sh
```

### Step 9: Run the Application (Quick Method)
```bash
./run.sh
```

### Step 10: Alternative - Manual Run
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```

### Step 11: Access the Application
Open browser: **http://localhost:5000**

---

## Verification

### Check if Everything Works

1. **Python is installed**:
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Virtual environment is created**:
   Check for `venv` folder in project directory

3. **Virtual environment is activated**:
   Look for `(venv)` prefix in terminal/command prompt

4. **Dependencies are installed**:
   ```bash
   pip list
   # Should show Flask, SQLAlchemy, qrcode, Pillow, etc.
   ```

5. **Flask app starts**:
   Should see output:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

6. **Web application loads**:
   Visit http://localhost:5000 in browser
   Should see login page

---

## Troubleshooting

### Issue: "Python is not recognized"
**Solution**: 
- Reinstall Python with "Add Python to PATH" checked
- Or add Python to PATH manually:
  - Windows: System Properties → Environment Variables
  - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python310`

### Issue: "Permission denied" on run.sh (macOS/Linux)
**Solution**:
```bash
chmod +x run.sh
./run.sh
```

### Issue: Virtual environment won't activate
**Solution**:
```bash
# Delete existing venv
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Create new one
python -m venv venv  # or python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate  # Windows
```

### Issue: "No module named Flask" when running
**Solution**:
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### Issue: Port 5000 is already in use
**Solution**:
```bash
# Kill process on port 5000 or change port
python app.py --port 5001
```

### Issue: Database permission error
**Solution**:
```bash
# Delete database and let it recreate
rm qr_generator.db  # macOS/Linux
del qr_generator.db  # Windows

# Restart application
python app.py
```

### Issue: "ModuleNotFoundError: No module named 'qrcode'"
**Solution**:
```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Static files not loading
**Solution**:
1. Check that `static/css/style.css` and `static/js/main.js` exist
2. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
3. Clear browser cache

### Issue: Logo upload not working
**Solution**:
1. Check `static/uploads` folder exists
2. Ensure file is PNG, JPG, or GIF
3. File size under 5MB
4. Restart application

### Issue: QR codes not generating
**Solution**:
1. Check `static/generated_qr` folder exists
2. Ensure write permissions on folder
3. Try clearing content and restarting

---

## Quick Reference Commands

### Windows
```bash
# Activate venv
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run app
python app.py

# Deactivate venv
deactivate
```

### macOS/Linux
```bash
# Activate venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run app
python app.py

# Deactivate venv
deactivate
```

---

## Environment Variables (Optional)

Create `.env` file in project root:

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

---

## Production Deployment

For deploying to production server:

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

3. Set environment to production:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-key
```

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review README.md for features and usage
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Review code comments in source files

---

**Installation Complete! 🎉**

Your QR Code Generator is now ready to use.

Start the application and visit http://localhost:5000 to begin generating QR codes!

---

*Last Updated: June 2026*
