# WatchStore — Setup Requirements

This document outlines everything needed to run the WatchStore project on a new laptop.

## 1. Prerequisites
Before setting up the project, ensure the following are installed on the system:
- **Python 3.8 or higher**: [Download from python.org](https://www.python.org/downloads/)
- **Node.js (Optional)**: Only needed if you plan to use advanced frontend tools, but not required for simple Django execution.

## 2. Project Components
The following Python packages must be installed:
1. **Django (v4.1.7)**: The core web framework.
2. **Pillow**: Required for image handling (product photos).

## 3. Setup Steps

### Step 1: Copy the Project
Copy the entire `watchproject` folder to the target laptop.

### Step 2: Create a Virtual Environment (Recommended)
Open a terminal (CMD or PowerShell) in the project folder and run:
```bash
python -m venv venv
```

### Step 3: Activate the Environment
- **Windows**: `.\venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

### Step 4: Install Dependencies
```bash
pip install django==4.1.7 pillow
```

### Step 5: Run the Server
```bash
python manage.py runserver
```

### Step 6: Admin Access
Access the admin panel at `http://127.0.0.1:8000/log/` using:
- **Username**: `admin`
- **Password**: `admin123`
