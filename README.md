# QR Code Generator - Complete Web Application

A production-ready QR Code Generator web application built with Python Flask, SQLAlchemy ORM, Bootstrap 5, and jQuery. Generate, customize, and manage QR codes with an intuitive and modern UI.

![QR Code Generator](https://img.shields.io/badge/Flask-v3.0.0-blue?style=flat-square&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![Database](https://img.shields.io/badge/Database-SQLite%2FMySQL-orange?style=flat-square&logo=database)

## 🌟 Features

### Authentication & Security
- ✅ User Registration with validation
- ✅ Secure Login with password hashing (PBKDF2)
- ✅ Session management with Flask-Login
- ✅ CSRF protection
- ✅ Password strength indicator
- ✅ Secure logout

### QR Code Generation
- ✅ Generate QR codes for multiple content types:
  - URLs (with auto http/https prefix)
  - Plain text
  - Email addresses (mailto: format)
  - Phone numbers (tel: format)
  - WiFi credentials (WIFI: format)
- ✅ Customizable QR code size (5-20)
- ✅ Foreground color customization
- ✅ Background color customization
- ✅ Logo upload and embedding in QR center
- ✅ Real-time preview before generation
- ✅ Download as PNG with transparency

### Dashboard
- ✅ Modern, responsive dashboard
- ✅ Statistics cards (total, by type)
- ✅ Recent QR codes display
- ✅ Quick action buttons
- ✅ Beautiful gradient designs

### History & Management
- ✅ View all generated QR codes
- ✅ Search functionality (by type, content, filename)
- ✅ Pagination support (10 items per page)
- ✅ Delete individual QR codes
- ✅ Bulk delete multiple QR codes
- ✅ Export history as CSV
- ✅ File cleanup on deletion

### User Interface
- ✅ Modern, gradient-based design
- ✅ Bootstrap 5 responsive framework
- ✅ Font Awesome icons
- ✅ Smooth animations and transitions
- ✅ Mobile-friendly layout
- ✅ Dark mode support ready
- ✅ Flash messages for user feedback

## 📋 Project Structure

```
qr_generator/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── models.py                       # Database models (User, QRCode)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── blueprints/                     # Flask blueprints
│   ├── __init__.py
│   ├── auth.py                    # Authentication (register, login, logout)
│   ├── dashboard.py               # Dashboard statistics
│   ├── qr_generator.py            # QR generation logic
│   └── history.py                 # QR history and search
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                  # Base template with navbar
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Dashboard with stats
│   ├── generate_qr.html           # QR generation form
│   └── history.html               # QR history page
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Custom CSS styles
│   ├── js/
│   │   └── main.js                # JavaScript utilities
│   ├── uploads/                   # Logo uploads
│   └── generated_qr/              # Generated QR codes
│
└── database/                       # Database storage
```

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone or Download
```bash
# Navigate to your desired location
cd ~/Desktop/QR  # or your preferred directory
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Or on Windows:
copy .env.example .env

# Edit .env file (optional - defaults work for development)
# FLASK_ENV=development
# SECRET_KEY=your-secret-key-here
```

### Step 6: Initialize Database
```bash
# Database will auto-initialize on first run
# Or manually create tables:
python
>>> from app import create_app
>>> from models import init_db
>>> app = create_app()
>>> init_db(app)
>>> exit()
```

### Step 7: (Optional) Create Admin User
```bash
python -m flask create-admin
# Follow the prompts to create an admin user
```

## 🎯 Step-by-Step Execution

### Run the Application

#### Option 1: Direct Python Execution
```bash
# Make sure virtual environment is activated
python app.py
```

#### Option 2: Using Flask CLI
```bash
# Make sure virtual environment is activated
set FLASK_APP=app.py  # Windows
# OR
export FLASK_APP=app.py  # macOS/Linux

flask run
```

#### Option 3: Production Run (Gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:create_app()
```

### Access the Application

Once running, open your browser and navigate to:
```
http://localhost:5000
```

### Test Account (Optional)
If you created an admin user, use those credentials to login. Otherwise:
1. Click "Register" button
2. Create a new account with username and password
3. Start generating QR codes!

## 📝 Usage Guide

### 1. Registration & Login
- Click "Register" on the login page
- Enter username, email, and password
- Password must be at least 6 characters
- Click "Create Account"
- Login with your credentials

 

### 2. Dashboard
- After login, you'll see the dashboard
- View statistics of your QR codes by type
- See recent QR codes
- Quick action buttons for fast navigation

### 3. Generate QR Code
- Click "Generate QR" in navbar or dashboard
- Select QR code type:
  - **URL**: For web links
  - **Text**: For any text content
  - **Email**: For email addresses (creates mailto: link)
  - **Phone**: For phone numbers (creates tel: link)
  - **WiFi**: For WiFi credentials
- Enter content
- Choose colors (foreground and background)
- Adjust size using slider
- (Optional) Upload logo image
- Click "Preview QR Code"
- Once satisfied, click "Generate & Download"

### 4. View History
- Click "History" in navbar
- See all your generated QR codes
- **Search**: Find QR codes by type, content, or filename
- **Download**: Get QR code as PNG
- **View**: Open QR code in new tab
- **Delete**: Remove individual QR codes
- **Bulk Delete**: Select multiple and delete at once
- **Export**: Download all records as CSV

### 5. QR Code Customization
- **Foreground Color**: Change the QR code pattern color
- **Background Color**: Change the QR code background
- **Logo**: Upload an image to embed in QR center (PNG, JPG, GIF)
- **Size**: Adjust module size for different scanning distances

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### QR Codes Table
```sql
CREATE TABLE qr_codes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    qr_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    logo_used BOOLEAN DEFAULT FALSE,
    fg_color VARCHAR(7) DEFAULT '#000000',
    bg_color VARCHAR(7) DEFAULT '#FFFFFF',
    qr_size INTEGER DEFAULT 10,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🔒 Security Features

- **Password Hashing**: PBKDF2-SHA256 with Werkzeug
- **Session Management**: Flask-Login with 7-day expiration
- **CSRF Protection**: Flask-WTF CSRF tokens
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **File Upload Validation**: Extension and size checks
- **Input Validation**: Client and server-side validation
- **Secure Cookies**: HttpOnly, Secure, SameSite flags

## 🛠️ Configuration Options

Edit `config.py` to customize:

```python
# Session lifetime
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# File upload limits
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///qr_generator.db'

# QR Code settings
QR_BOX_SIZE = 10
QR_BORDER = 4
```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Dashboard
- `GET /dashboard` - Dashboard page

### QR Generation
- `GET /qr/generate` - QR generation form
- `POST /qr/api/preview` - Preview QR code (JSON)
- `POST /qr/api/create` - Create and save QR code
- `GET /qr/download/<qr_id>` - Download QR code PNG

### History & Search
- `GET /history/` - QR code history page
- `POST /history/api/search` - Search QR codes (JSON)
- `DELETE /history/api/delete/<qr_id>` - Delete QR code
- `POST /history/api/bulk-delete` - Bulk delete QR codes
- `GET /history/api/export` - Export as CSV

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError" when running
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database not found
**Solution**: Database will auto-create. If needed, manually initialize:
```bash
python -c "from app import create_app; from models import init_db; app = create_app(); init_db(app)"
```

### Issue: Port 5000 already in use
**Solution**: Run on different port
```bash
python app.py --port 5001
```

### Issue: Logo not showing in QR code
**Solution**: Ensure file is PNG, JPG, or GIF and under 5MB

### Issue: QR code too large/small
**Solution**: Adjust QR size slider on generate page (5-20)

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-Login | 0.6.3 | Session management |
| Flask-WTF | 1.2.1 | Form handling |
| Werkzeug | 3.0.1 | Password hashing |
| qrcode | 7.4.2 | QR generation |
| Pillow | 10.1.0 | Image processing |
| python-dotenv | 1.0.0 | Environment variables |
| WTForms | 3.1.1 | Form validation |
| email-validator | 2.1.0 | Email validation |

## 🌐 Deployment

### Using Gunicorn (Recommended for Production)
```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Using Waitress (Windows Compatible)
```bash
# Install waitress
pip install waitress

# Run
waitress-serve --port=5000 "app:create_app()"
```

### Environment for Production
```bash
FLASK_ENV=production
SECRET_KEY=generate-a-secure-random-key
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer Notes

### Adding New Features

1. **New Blueprint**: Create file in `blueprints/` folder
2. **Database Model**: Add to `models.py`
3. **Template**: Add HTML in `templates/` folder
4. **Static Files**: Add CSS/JS in `static/` folders
5. **Register Blueprint**: Add to `app.py`

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Handle exceptions gracefully
- Use SQLAlchemy ORM for database operations
- Validate all user inputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Flask documentation: https://flask.palletsprojects.com/

## 🎉 Conclusion

You now have a fully functional QR Code Generator application! Customize it further, deploy it to your server, or use it as a learning resource for Flask development.

Happy QR Code Generating! 🚀

---

**Built with ❤️ using Flask and Bootstrap**
#   q r _ g e n e r a t o r  
 