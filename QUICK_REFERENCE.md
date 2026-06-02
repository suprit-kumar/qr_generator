# QR Code Generator - Quick Reference Guide

Fast lookup guide for common tasks and commands.

---

## 🚀 Quick Start

### Windows
```bash
cd qr_generator
run.bat
# Open http://localhost:5000
```

### macOS/Linux
```bash
cd qr_generator
chmod +x run.sh
./run.sh
# Open http://localhost:5000
```

---

## 📋 Manual Commands

### Setup Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Windows Command Prompt)
.\venv\Scripts\activate

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
python app.py
```

### Deactivate Environment
```bash
deactivate
```

---

## 🔗 Important URLs

| Page | URL |
|------|-----|
| Home | http://localhost:5000/ |
| Login | http://localhost:5000/auth/login |
| Register | http://localhost:5000/auth/register |
| Dashboard | http://localhost:5000/dashboard |
| Generate QR | http://localhost:5000/qr/generate |
| History | http://localhost:5000/history/ |

---

## 🔑 Test Credentials

**Create new user via registration form:**
- Username: `testuser`
- Email: `test@example.com`
- Password: `password123`

---

## 📁 Directory Structure Quick View

```
qr_generator/
├── app.py                    # Run this file
├── config.py                 # Configuration
├── models.py                 # Database models
├── blueprints/              # Route handlers
│   ├── auth.py
│   ├── dashboard.py
│   ├── qr_generator.py
│   └── history.py
├── templates/               # HTML pages
├── static/                  # CSS, JS, uploads
│   ├── css/style.css
│   ├── js/main.js
│   ├── uploads/             # Logo uploads
│   └── generated_qr/        # Generated QR codes
└── requirements.txt         # Dependencies
```

---

## 🎯 Common Tasks

### Create Admin User
```bash
python -m flask create-admin
```

### Reset Database
```bash
# Delete database file
rm qr_generator.db          # macOS/Linux
del qr_generator.db         # Windows

# Restart application - DB will auto-create
python app.py
```

### Check Python Version
```bash
python --version
python3 --version
```

### List Installed Packages
```bash
pip list
```

### Show Pip Version
```bash
pip --version
```

---

## 🔍 Troubleshooting Quick Fix

### Issue: Port 5000 already in use
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000

# Kill process
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>

# Or change Flask port
python app.py --port 5001
```

### Issue: Module not found
```bash
# Ensure venv is activated (should see (venv) prefix)
# Then reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Permission denied (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Issue: Database locked
```bash
# Delete database and restart
rm qr_generator.db
python app.py
```

---

## 📄 Files to Edit

| Purpose | File |
|---------|------|
| Change secret key | `config.py` |
| Add routes | `blueprints/*.py` |
| Change styles | `static/css/style.css` |
| Modify templates | `templates/*.html` |
| Add Python code | `app.py` or blueprints |

---

## 🗄️ Database

### SQLite File Location
```
qr_generator/qr_generator.db
```

### Tables
- `users` - User accounts
- `qr_codes` - Generated QR codes

### View Database
```bash
# Install sqlite3 CLI (if not installed)
# macOS: brew install sqlite
# Linux: apt-get install sqlite3
# Windows: Download from https://www.sqlite.org/download.html

# Open database
sqlite3 qr_generator.db

# Common commands
.tables                 # Show all tables
.schema users          # Show users schema
.schema qr_codes       # Show qr_codes schema
SELECT * FROM users;   # View all users
SELECT COUNT(*) FROM qr_codes;  # Count QR codes
.quit                  # Exit
```

---

## 🔐 Security Checklist

Before deployment:
- [ ] Change SECRET_KEY in config.py
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Use strong database password
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Disable debug mode
- [ ] Set up CORS properly
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Backup database

---

## 📊 Code Files Overview

### app.py (Main Application)
- Application factory
- Blueprint registration
- Error handlers
- CLI commands

### config.py (Configuration)
- Development settings
- Production settings
- Database URI
- File upload settings

### models.py (Database)
- User model
- QRCode model
- Database initialization

### auth.py (Authentication)
- Register route
- Login route
- Logout route

### dashboard.py (Dashboard)
- Statistics calculation
- Recent QR codes

### qr_generator.py (QR Creation)
- QR code generation
- Logo embedding
- File saving
- Preview API

### history.py (History Management)
- Search functionality
- Pagination
- Delete operations
- CSV export

---

## 🎨 Common CSS Classes

### Bootstrap Classes
```html
<!-- Containers -->
<div class="container">       <!-- Fixed width -->
<div class="container-fluid"> <!-- Full width -->

<!-- Grid -->
<div class="row">
  <div class="col-md-6">      <!-- 50% on medium+ -->
  <div class="col-lg-4">      <!-- 33% on large+ -->

<!-- Spacing -->
<div class="mb-3">            <!-- Margin bottom -->
<div class="p-4">             <!-- Padding -->
<div class="mt-5">            <!-- Margin top -->

<!-- Colors -->
<button class="btn btn-primary">    <!-- Blue -->
<button class="btn btn-success">    <!-- Green -->
<button class="btn btn-danger">     <!-- Red -->

<!-- Text -->
<p class="text-muted">              <!-- Gray -->
<p class="text-center">             <!-- Centered -->
<h1 class="mb-3">                   <!-- Heading with margin -->
```

### Custom Classes
```css
/* Gradients */
.bg-gradient-info { /* gradient background */ }

/* Shadows */
.shadow-sm  /* Small shadow */
.shadow-lg  /* Large shadow */

/* Cards */
.card       /* Card container */
.card-body  /* Card content */
```

---

## 💾 Database Queries

### User Related
```sql
-- Get user count
SELECT COUNT(*) FROM users;

-- Get user by username
SELECT * FROM users WHERE username = 'testuser';

-- Get user by email
SELECT * FROM users WHERE email = 'test@example.com';
```

### QR Code Related
```sql
-- Get all QR codes
SELECT * FROM qr_codes;

-- Count by type
SELECT qr_type, COUNT(*) FROM qr_codes GROUP BY qr_type;

-- Get QR codes for user
SELECT * FROM qr_codes WHERE user_id = 1;

-- Get recent QR codes
SELECT * FROM qr_codes ORDER BY created_at DESC LIMIT 5;

-- Delete old QR codes
DELETE FROM qr_codes WHERE created_at < date('now', '-30 days');
```

---

## 🐍 Python Shortcuts

### Quick Database Access
```python
from app import create_app
from models import db, User, QRCode

app = create_app()

with app.app_context():
    # Get all users
    users = User.query.all()
    
    # Get user by id
    user = User.query.get(1)
    
    # Get user QR codes
    qr_codes = user.qr_codes.all()
    
    # Count QR codes by type
    from sqlalchemy import func
    counts = db.session.query(
        QRCode.qr_type,
        func.count(QRCode.id)
    ).group_by(QRCode.qr_type).all()
```

---

## 🌐 API Quick Reference

### Authentication
```
POST /auth/register    # Create account
POST /auth/login       # Login
GET /auth/logout       # Logout
```

### QR Generation
```
GET /qr/generate              # Form page
POST /qr/api/preview          # Preview QR
POST /qr/api/create           # Create QR
GET /qr/download/<id>         # Download QR
```

### History
```
GET /history/                     # History page
POST /history/api/search          # Search QR
DELETE /history/api/delete/<id>   # Delete QR
POST /history/api/bulk-delete     # Bulk delete
GET /history/api/export           # Export CSV
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| INSTALLATION.md | Setup guide |
| API.md | API reference |
| PROJECT_SUMMARY.md | Architecture overview |
| DELIVERABLES.md | Complete checklist |
| QUICK_REFERENCE.md | This file |

---

## 🎓 Learning Resources

### Official Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Bootstrap: https://getbootstrap.com/
- jQuery: https://jquery.com/

### Python
- PEP 8 Style Guide: https://www.python.org/dev/peps/pep-0008/
- Python Docs: https://docs.python.org/3/

---

## 🔧 Useful Tools

### Code Editors
- VS Code (Recommended)
- PyCharm
- Sublime Text

### Browser DevTools
- Chrome DevTools (F12)
- Firefox Developer (F12)
- Safari Web Inspector

### Database Tools
- SQLite Browser
- DBeaver
- TablePlus

### API Testing
- Postman
- Insomnia
- curl

---

## 🚀 Deployment Quick Steps

### Local to Live
1. Create `.env` file with production settings
2. Set `FLASK_ENV=production`
3. Generate secure `SECRET_KEY`
4. Install Gunicorn: `pip install gunicorn`
5. Run: `gunicorn -w 4 app:create_app()`

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://user:pass@host/db
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

---

## 📞 Help Resources

1. Check **INSTALLATION.md** for setup issues
2. Check **API.md** for endpoint details
3. Check **README.md** for features
4. Read code comments in files
5. Check stack trace in terminal
6. Use Python debugger: `python -m pdb app.py`

---

## ⏱️ Keyboard Shortcuts

### Flask Development
| Shortcut | Action |
|----------|--------|
| Ctrl+C | Stop server |
| Ctrl+S | Save file (auto-reload) |
| F5 | Hard refresh browser |
| Ctrl+Shift+R | Clear cache & reload |

### Common Commands
```bash
Ctrl+Alt+T   # Open terminal (Linux)
Cmd+Space    # Spotlight search (macOS)
Win+R        # Run command (Windows)
```

---

## 🎯 Checklist

### Development
- [ ] Created virtual environment
- [ ] Installed dependencies
- [ ] Application runs locally
- [ ] Can register/login
- [ ] Can generate QR codes
- [ ] Database saves correctly
- [ ] All pages load

### Before Deployment
- [ ] Changed SECRET_KEY
- [ ] Updated database URL
- [ ] Set production settings
- [ ] Tested all features
- [ ] Verified security
- [ ] Backed up database

---

## 💡 Tips & Tricks

1. **Use virtual environment** - Always use venv for clean isolation
2. **Read error messages** - They tell you exactly what's wrong
3. **Check Flask debug toolbar** - Install `flask-debugtoolbar` for debugging
4. **Use logging** - Add `logging.debug()` to debug code
5. **Test thoroughly** - Test all features before deployment
6. **Keep backups** - Always backup your database
7. **Read documentation** - Check docs before asking questions
8. **Use version control** - Track changes with git

---

## 🎉 You're Ready!

Everything is set up and ready to use. Start with:
```bash
cd qr_generator
python app.py
# Visit http://localhost:5000
```

Happy QR Code Generating! 🚀

---

*Quick Reference Guide - June 2026*
