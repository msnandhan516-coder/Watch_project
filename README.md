# ⌚ WatchStore Pro

> **A Premium Luxury Watch Ecommerce Platform** built with Django & SQLite

![WatchStore Pro](https://img.shields.io/badge/Django-4.1.7-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?style=flat-square&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Software Requirements](#software-requirements)
4. [Installation Guide](#installation-guide)
5. [Database Table Structure](#database-table-structure)
6. [Running the Project](#running-the-project)
7. [Default Admin Setup](#default-admin-setup)
8. [Project Structure](#project-structure)
9. [Page Routes](#page-routes)
10. [Troubleshooting](#troubleshooting)

---

## 🧾 Project Overview

**WatchStore Pro** is a full-stack Django web application for a luxury watch store. It includes:
- A public landing page showcasing the product catalog
- Customer registration, login, and shopping flow (add to cart → payment → order history)
- A complete admin panel to manage products, process orders, and view sales analytics

---

## ✨ Features

### Customer Side
- 🛍️ Browse watches with search and category filters
- 🛒 Add to cart → checkout → payment confirmation
- 📦 Track order history and status
- 🔐 Change password with strength meter
- 📱 Fully responsive on all devices

### Admin Side
- 📊 Dashboard with live stats (products, orders, revenue)
- ➕ Add, edit, delete watches with image upload
- 🧾 Process new orders → mark as invoiced
- 📈 Sales analytics and reports
- 🔍 Search products in the admin catalog

### Design
- 🌑 Premium dark luxury theme (deep space + electric gold)
- 🪟 Glassmorphism cards with backdrop blur
- ✨ Scroll reveal animations, floating product images
- 💳 Animated credit card visual on payment page
- 🔑 Password strength meter on registration/change password

---

## 💻 Software Requirements

### 1. Python
| Requirement | Version |
|---|---|
| **Python** | **3.10, 3.11, or 3.12** (3.11 recommended) |

**Download:** https://www.python.org/downloads/

> ⚠️ During installation, check **"Add Python to PATH"**

**Verify:** Open Command Prompt or PowerShell and run:
```bash
python --version
```
Expected output: `Python 3.11.x`

---

### 2. pip (Python Package Manager)
pip comes pre-installed with Python 3.x.

**Verify:**
```bash
pip --version
```

---

### 3. Django
| Package | Version |
|---|---|
| Django | 4.1.7 |
| Pillow | 9.4.0 |

These are installed via the virtual environment (see Installation Guide).

---

### 4. Git (Optional but recommended)
**Download:** https://git-scm.com/downloads

---

### 5. SQLite (Included with Python)
SQLite is **built into Python** — no separate installation needed.

---

### 6. Web Browser
Any modern browser:
- Google Chrome (recommended)
- Mozilla Firefox
- Microsoft Edge

---

## 🚀 Installation Guide

### Step 1: Clone or Copy the Project
If using Git:
```bash
git clone <your-repo-url>
cd watchproject/watchproject
```
Or simply copy the `watchproject/` folder to your machine.

---

### Step 2: Navigate to the Project Root
```powershell
cd d:\watchproject\watchproject
```
> This folder contains `manage.py`

---

### Step 3: Create a Virtual Environment
```bash
python -m venv venv
```

---

### Step 4: Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 5: Install Required Packages
```bash
pip install Django==4.1.7 Pillow==9.4.0
```

---

### Step 6: Apply Database Migrations
```bash
python manage.py migrate
```

---

### Step 7: Create Admin User
```bash
python manage.py shell
```
In the shell, run:
```python
from myapp.models import signup
signup.objects.create(
    name='Admin', first_name='Admin', last_name='User',
    email='admin@watchstore.com', phone='9999999999',
    uname='admin', pas='admin123', rights='A', is_active=True
)
exit()
```

---

### Step 8: Run the Development Server
```bash
python manage.py runserver
```

---

### Step 9: Open in Browser
Navigate to: **http://127.0.0.1:8000/**

---

## 🗄️ Database Table Structure

The project uses **SQLite3** as its database (`db.sqlite3`).

---

### Table 1: `myapp_signup` — User Accounts

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO | User ID |
| `name` | VARCHAR(100) | NOT NULL | Full name |
| `first_name` | VARCHAR(50) | NULL | First name |
| `last_name` | VARCHAR(50) | NULL | Last name |
| `email` | VARCHAR(100) | NULL | Email address |
| `phone` | VARCHAR(15) | NULL | 10-digit phone |
| `uname` | VARCHAR(30) | UNIQUE | Username for login |
| `pas` | VARCHAR(128) | NOT NULL | Password |
| `rights` | VARCHAR(10) | DEFAULT 'U' | 'A' = Admin, 'U' = User |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active status |
| `created_at` | DATETIME | AUTO (now) | Registration timestamp |
| `last_login` | DATETIME | NULL | Last login timestamp |

---

### Table 2: `myapp_watchstock` — Products / Inventory

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO | Product ID |
| `wname` | VARCHAR(100) | UNIQUE, NOT NULL | Watch name |
| `brand` | VARCHAR(50) | NULL | Brand name (e.g. Rolex) |
| `category` | VARCHAR(20) | NULL | Luxury/Sport/Casual/Smart/Classic |
| `description` | TEXT | NULL | Product description |
| `price` | INTEGER | NOT NULL | Price in ₹ |
| `qty` | INTEGER | NOT NULL | Stock quantity |
| `photo` | VARCHAR | NOT NULL | Image file path (uploaded) |
| `is_featured` | BOOLEAN | DEFAULT FALSE | Show on homepage |

---

### Table 3: `myapp_watchcart` — Shopping Cart

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO | Cart item ID |
| `slno` | INTEGER | NOT NULL | Serial number within user's cart |
| `pname` | VARCHAR(100) | NOT NULL | Watch name |
| `rate` | INTEGER | NOT NULL | Unit price at time of adding |
| `qty` | INTEGER | NOT NULL | Quantity added |
| `total` | INTEGER | NOT NULL | rate × qty |
| `userid` | INTEGER | NOT NULL | FK → `myapp_signup.id` |

---

### Table 4: `myapp_watchsales` — Orders / Sales Header

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO | Internal ID |
| `salesno` | INTEGER | UNIQUE, NOT NULL | Order number |
| `salesdate` | DATE | DEFAULT today | Order date |
| `userid` | INTEGER | NOT NULL | Customer ID |
| `uname` | VARCHAR(100) | NOT NULL | Customer name |
| `shipment` | VARCHAR(500) | NOT NULL | Delivery address |
| `phone` | VARCHAR(15) | NOT NULL | Customer phone |
| `cardno` | VARCHAR(40) | NOT NULL | Masked card number |
| `total` | INTEGER | NOT NULL | Order total |
| `status` | VARCHAR(30) | DEFAULT 'New Order' | Order status |
| `notes` | TEXT | NULL | Additional notes |

**Status Values:** `New Order` → `Processing` → `Shipped` → `Delivered` / `Cancelled`

---

### Table 5: `myapp_watchsalessub` — Order Line Items

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO | Sub-item ID |
| `salesno` | INTEGER | NOT NULL | FK → `myapp_watchsales.salesno` |
| `slno` | INTEGER | NOT NULL | Item serial number |
| `pname` | VARCHAR(100) | NOT NULL | Watch name |
| `rate` | INTEGER | NOT NULL | Unit price |
| `qty` | INTEGER | NOT NULL | Quantity ordered |
| `total` | INTEGER | NOT NULL | subtotal for this line |

---

## ▶️ Running the Project

```bash
# Activate virtual environment (Windows PowerShell)
cd d:\watchproject\watchproject
venv\Scripts\Activate.ps1

# Start the server
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

### Stop the Server
Press `Ctrl + C` in the terminal.

---

## 🔑 Default Admin Setup

To create the admin account, use the Django shell (as shown in Step 7) or use the registration page with rights manually set to `'A'` via Django admin.

**Default credentials (after running Step 7):**
| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

> 🔒 Change the password immediately after first login via `/passs/`

---

## 📁 Project Structure

```
watchproject/
└── watchproject/           ← Project root (contains manage.py)
    ├── manage.py
    ├── db.sqlite3          ← SQLite database
    ├── README.md           ← This file
    ├── media/
    │   └── images/         ← Uploaded product photos
    ├── venv/               ← Virtual environment
    ├── myapp/              ← Main Django application
    │   ├── models.py       ← Database models
    │   ├── views.py        ← Business logic & validations
    │   ├── urls.py         ← URL routing
    │   ├── admin.py        ← Django admin config
    │   └── templates/      ← All HTML pages (23 templates)
    │       ├── base.html
    │       ├── index.html
    │       ├── login.html
    │       ├── reg.html
    │       ├── userpage.html
    │       ├── order.html
    │       ├── vieworder.html
    │       ├── payment.html
    │       ├── userpayment.html
    │       ├── mysales.html
    │       ├── mysalessub.html
    │       ├── changepass.html
    │       ├── adminpanel.html
    │       ├── AdminAddwatch.html
    │       ├── AdminListwatch.html
    │       ├── AdminEditwatch.html
    │       ├── AdminInvoice.html
    │       ├── AdminInvoiceSub.html
    │       ├── AdminSalesReport.html
    │       ├── AdminSalesSub.html
    │       └── notfound.html
    └── watchproject/       ← Django settings package
        ├── settings.py
        ├── urls.py
        ├── wsgi.py
        └── static/
            └── css/
                └── luxe.css   ← Premium design system
```

---

## 🗺️ Page Routes

| URL | Page | Access |
|---|---|---|
| `/` | Home / Landing Page | Public |
| `/reg/` | Register | Public |
| `/log/` | Login | Public |
| `/logout/` | Logout | Logged in |
| `/up/` | Shop / Product Grid | User |
| `/ord/<id>/` | Product Order Page | User |
| `/vc/` | View Cart | User |
| `/pay/` | Checkout | User |
| `/upay/` | Payment Form | User |
| `/myp/` | My Orders | User |
| `/ms/<salesno>/` | Order Detail | User |
| `/passs/` | Change Password | User |
| `/sap/` | Admin Dashboard | Admin |
| `/aap/` | Add Watch | Admin |
| `/aapl/` | Product List | Admin |
| `/edit/<id>/` | Edit Watch | Admin |
| `/del/<id>/` | Delete Watch | Admin |
| `/inv/` | Orders (New) | Admin |
| `/aumd/<salesno>/` | Order Items | Admin |
| `/invn/<id>/` | Mark as Invoiced | Admin |
| `/sreport/` | Sales Report | Admin |
| `/aumd1/<salesno>/` | Sales Sub-detail | Admin |

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Windows — find and kill the process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart
python manage.py runserver
```

### Module Not Found / Import Errors
```bash
# Make sure venv is activated and packages installed
venv\Scripts\Activate.ps1
pip install Django==4.1.7 Pillow==9.4.0
```

### Images Not Loading
- Ensure `media/` folder exists inside the project root
- Check `MEDIA_ROOT` and `MEDIA_URL` in `settings.py`
- Run with `python manage.py runserver` (DEBUG=True required for media serving)

### Migration Errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Missing (CSS/JS not loading)
```bash
python manage.py collectstatic
```
Or ensure `DEBUG = True` in `settings.py` for development.

---

## 📞 Support

For issues, open a GitHub issue or contact the project maintainer.

---

*Built with ❤️ using Django 4.1.7 | WatchStore Pro © 2026*
