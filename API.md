# QR Code Generator - API Documentation

Complete API reference for the QR Code Generator application.

## Base URL
```
http://localhost:5000
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require user authentication via Flask-Login session.

### Session Management
- Sessions are maintained using Flask-Login
- Session cookies expire after 7 days
- CSRF protection is enabled for all POST requests

---

## API Endpoints

### 1. Authentication Endpoints

#### Register New User
```
POST /auth/register
```

**Parameters** (Form Data):
- `username` (string, required): 3-80 characters, alphanumeric
- `email` (string, required): Valid email format
- `password` (string, required): Minimum 6 characters
- `confirm_password` (string, required): Must match password

**Success Response** (302 Redirect):
- Redirects to login page
- Flash message: Account created successfully

**Error Response**:
- Flash message with validation error
- Redirects back to register page

**Example**:
```bash
curl -X POST http://localhost:5000/auth/register \
  -d "username=john_doe&email=john@example.com&password=password123&confirm_password=password123"
```

---

#### User Login
```
POST /auth/login
```

**Parameters** (Form Data):
- `username` (string, required): Registered username
- `password` (string, required): User password
- `remember_me` (checkbox, optional): Remember for 7 days

**Success Response** (302 Redirect):
- Sets session cookie
- Redirects to dashboard
- Flash message: Welcome back!

**Error Response** (302 Redirect):
- Flash message: Invalid username or password
- Redirects back to login page

**Example**:
```bash
curl -X POST http://localhost:5000/auth/login \
  -d "username=john_doe&password=password123" \
  -c cookies.txt
```

---

#### User Logout
```
GET /auth/logout
```

**Required**: User must be authenticated

**Success Response** (302 Redirect):
- Clears session
- Redirects to login page
- Flash message: You have been logged out

**Example**:
```bash
curl http://localhost:5000/auth/logout \
  -b cookies.txt
```

---

### 2. Dashboard Endpoints

#### Get Dashboard
```
GET /dashboard
```

**Required**: User must be authenticated

**Response**: HTML page with statistics

**Data Returned**:
- Total QR codes count
- QR codes by type breakdown
- Recent 5 QR codes
- User information

**Example**:
```bash
curl http://localhost:5000/dashboard \
  -b cookies.txt
```

---

### 3. QR Generation Endpoints

#### Get QR Generation Form
```
GET /qr/generate
```

**Required**: User must be authenticated

**Response**: HTML form page

**Example**:
```bash
curl http://localhost:5000/qr/generate \
  -b cookies.txt
```

---

#### Preview QR Code
```
POST /qr/api/preview
```

**Required**: User must be authenticated

**Headers**:
```
Content-Type: application/json
```

**JSON Body**:
```json
{
  "qr_type": "url",           // url, text, email, phone, wifi
  "content": "https://example.com",
  "fg_color": "#000000",      // Optional, default: #000000
  "bg_color": "#FFFFFF",      // Optional, default: #FFFFFF
  "qr_size": 10               // Optional, default: 10, range: 5-20
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "message": "Content is required"
}
```

**Validation Rules**:
- `qr_type` must be one of: url, text, email, phone, wifi
- `content` required and non-empty
- `fg_color` and `bg_color` must be valid hex colors

**Example**:
```bash
curl -X POST http://localhost:5000/qr/api/preview \
  -H "Content-Type: application/json" \
  -d '{"qr_type":"url","content":"https://example.com"}' \
  -b cookies.txt
```

---

#### Create QR Code
```
POST /qr/api/create
```

**Required**: User must be authenticated

**Parameters** (Form Data):
- `qr_type` (string, required): url, text, email, phone, wifi
- `content` (string, required): Content to encode
- `fg_color` (string, optional): Foreground color hex (default: #000000)
- `bg_color` (string, optional): Background color hex (default: #FFFFFF)
- `qr_size` (integer, optional): Box size 5-20 (default: 10)
- `logo` (file, optional): Logo image (PNG, JPG, GIF, max 5MB)

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "QR code generated successfully",
  "qr_id": 42,
  "qr_url": "/static/generated_qr/20260602_150530_123456_qr_url.png",
  "download_url": "/qr/download/42"
}
```

**Error Response** (400/500):
```json
{
  "success": false,
  "message": "Error message here"
}
```

**QR Type Specific Content**:

**URL**:
```
https://example.com
```
Auto-prefixes with https:// if missing

**Text**:
```
Any text content
```

**Email**:
```
user@example.com
```
Encoded as: mailto:user@example.com

**Phone**:
```
+1 (555) 123-4567
```
Extracted digits and encoded as: tel:+15551234567

**WiFi**:
```json
{
  "ssid": "NetworkName",
  "password": "password123",
  "security": "WPA"
}
```
Encoded as: WIFI:T:WPA;S:NetworkName;P:password123;;

**Example**:
```bash
curl -X POST http://localhost:5000/qr/api/create \
  -F "qr_type=url" \
  -F "content=https://github.com" \
  -F "fg_color=#667eea" \
  -F "bg_color=#FFFFFF" \
  -F "qr_size=12" \
  -b cookies.txt
```

---

#### Download QR Code
```
GET /qr/download/<qr_id>
```

**Required**: User must be authenticated and own the QR code

**Parameters**:
- `qr_id` (integer, required): ID of QR code to download

**Success Response** (200 OK):
- File download: PNG image

**Error Response**:
- 404: QR code not found
- 403: Unauthorized (not owner)

**Example**:
```bash
curl http://localhost:5000/qr/download/42 \
  -b cookies.txt \
  -o qr_code.png
```

---

### 4. History & Search Endpoints

#### Get QR History Page
```
GET /history/?page=1&search=query
```

**Required**: User must be authenticated

**Query Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `search` (string, optional): Search query

**Response**: HTML page with QR code table

**Example**:
```bash
curl "http://localhost:5000/history/?page=1&search=url" \
  -b cookies.txt
```

---

#### Search QR Codes (API)
```
POST /history/api/search
```

**Required**: User must be authenticated

**Headers**:
```
Content-Type: application/json
```

**JSON Body**:
```json
{
  "query": "search text",  // Optional, empty string returns all
  "page": 1                // Optional, default: 1
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "qr_codes": [
    {
      "id": 1,
      "type": "url",
      "content": "https://github.com/...",
      "file_name": "20260602_150530_123456_qr_url.png",
      "created_at": "2026-06-02 15:05:30",
      "file_url": "/static/generated_qr/20260602_150530_123456_qr_url.png",
      "download_url": "/qr/download/1"
    }
  ],
  "total": 42,
  "pages": 5,
  "current_page": 1
}
```

**Search Fields**:
- QR type (exact match)
- Content (partial match, case-insensitive)
- File name (partial match, case-insensitive)

**Example**:
```bash
curl -X POST http://localhost:5000/history/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"github","page":1}' \
  -b cookies.txt
```

---

#### Delete QR Code
```
DELETE /history/api/delete/<qr_id>
```

**Required**: User must be authenticated and own the QR code

**Parameters**:
- `qr_id` (integer, required): ID of QR code to delete

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "QR code deleted successfully"
}
```

**Error Response**:
- 404: QR code not found
- 403: Unauthorized

**Example**:
```bash
curl -X DELETE http://localhost:5000/history/api/delete/42 \
  -b cookies.txt
```

---

#### Bulk Delete QR Codes
```
POST /history/api/bulk-delete
```

**Required**: User must be authenticated

**Headers**:
```
Content-Type: application/json
```

**JSON Body**:
```json
{
  "qr_ids": [1, 2, 3, 4, 5]
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "5 QR codes deleted successfully"
}
```

**Error Response** (400/403):
```json
{
  "success": false,
  "message": "Error message"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/history/api/bulk-delete \
  -H "Content-Type: application/json" \
  -d '{"qr_ids":[1,2,3]}' \
  -b cookies.txt
```

---

#### Export QR History as CSV
```
GET /history/api/export
```

**Required**: User must be authenticated

**Success Response** (200 OK):
```json
{
  "success": true,
  "csv_data": "ID,Type,Content,...\n1,url,https://...\n2,text,Some text\n...",
  "filename": "qr_history_20260602_150530.csv"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Error message"
}
```

**CSV Columns**:
- ID
- Type
- Content (first 100 chars)
- File Name
- Logo Used
- Foreground Color
- Background Color
- Created At

**Example**:
```bash
curl http://localhost:5000/history/api/export \
  -b cookies.txt
```

---

## Response Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful API request |
| 302 | Found | Redirect (login, logout) |
| 400 | Bad Request | Invalid input/validation error |
| 403 | Forbidden | Unauthorized (not owner) |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal error |

---

## Error Handling

All error responses follow this format:

### HTML Pages (Form submissions)
- Redirects to previous page
- Flash message displayed to user

### JSON APIs
```json
{
  "success": false,
  "message": "Human-readable error message"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding:
- Login attempt limits
- QR generation rate limits
- API call throttling

---

## CORS

CORS is not enabled by default. To enable for cross-origin requests:

```python
# Add to app.py
from flask_cors import CORS
CORS(app)
```

---

## Authentication Example

### Complete Login + Generate QR Workflow

```bash
#!/bin/bash

# 1. Register
curl -X POST http://localhost:5000/auth/register \
  -d "username=testuser&email=test@example.com&password=pass123&confirm_password=pass123"

# 2. Login (save cookies)
curl -X POST http://localhost:5000/auth/login \
  -d "username=testuser&password=pass123" \
  -c cookies.txt

# 3. Preview QR
curl -X POST http://localhost:5000/qr/api/preview \
  -H "Content-Type: application/json" \
  -d '{"qr_type":"url","content":"https://example.com"}' \
  -b cookies.txt

# 4. Generate QR
curl -X POST http://localhost:5000/qr/api/create \
  -F "qr_type=url" \
  -F "content=https://example.com" \
  -b cookies.txt

# 5. Search QR
curl -X POST http://localhost:5000/history/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"example","page":1}' \
  -b cookies.txt

# 6. Logout
curl http://localhost:5000/auth/logout \
  -b cookies.txt
```

---

## WebSocket Support

WebSocket support is not currently implemented. For real-time features, consider:
- Flask-SocketIO for real-time updates
- Server-sent events for notifications

---

## API Changelog

### Version 1.0 (Current)
- Initial API release
- Basic CRUD operations for QR codes
- User authentication
- Search and filtering
- Bulk operations

---

## Best Practices

1. **Always validate input** on both client and server
2. **Use HTTPS in production** for secure communication
3. **Handle errors gracefully** and provide meaningful messages
4. **Implement rate limiting** to prevent abuse
5. **Log all API requests** for monitoring
6. **Use appropriate HTTP methods**: GET for retrieval, POST for creation, DELETE for deletion
7. **Return consistent response formats**
8. **Implement proper error handling** with appropriate status codes

---

## Debugging API Calls

### Using cURL
```bash
# Verbose output
curl -v http://localhost:5000/endpoint

# Show headers
curl -i http://localhost:5000/endpoint

# Save response to file
curl http://localhost:5000/endpoint > response.txt
```

### Using Python Requests
```python
import requests
import json

# POST request
response = requests.post(
    'http://localhost:5000/qr/api/preview',
    json={'qr_type': 'url', 'content': 'https://example.com'},
    cookies={'session': 'your_session_id'}
)

print(json.dumps(response.json(), indent=2))
```

### Using JavaScript Fetch
```javascript
fetch('http://localhost:5000/qr/api/preview', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    qr_type: 'url',
    content: 'https://example.com'
  }),
  credentials: 'include'  // Include cookies
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Future API Enhancements

- [ ] API key authentication
- [ ] OAuth 2.0 support
- [ ] Rate limiting
- [ ] API versioning
- [ ] Webhook support
- [ ] GraphQL endpoint
- [ ] WebSocket for real-time updates
- [ ] Batch operations
- [ ] Advanced filtering and sorting

---

*Last Updated: June 2026*
