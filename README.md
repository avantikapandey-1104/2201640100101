# 2201640100101

# URL Shortener Microservice

This repository contains my **Backend Test Submission** for the AffordMed Campus Hiring Evaluation.  
It includes a Flask-based microservice implementation of a **URL Shortener**, with logging middleware, analytics, error handling, and configurable expiry.

---

## 📌 Project Structure
├── logging-middleware/
│ └── logger.py # Logging Middleware Implementation
│
├── backend-test-submission/
│ ├── app.py # Main Flask Application
│ ├── url_store.py # In-memory URL store & analytics
│ ├── logger.py # Middleware copy for backend
│ └── architecture.png # Architecture diagram (added by me)
│
└── README.md # Project Documentation


---

## ⚙️ Features Implemented

- **Logging Middleware**: All requests are logged with timestamp, HTTP method, and path.  
- **Microservice Architecture**: Independent service exposing RESTful endpoints.  
- **Create Short URL** (`POST /shorturls`)  
  - Accepts long URL, optional validity (minutes), optional custom shortcode.  
  - Defaults validity to **30 minutes** if not provided.  
  - Ensures **globally unique shortcodes**.  
- **Redirection** (`GET /<shortcode>`)  
  - Redirects to original URL if valid and not expired.  
  - Records click details (timestamp, source, geo-location header).  
- **Retrieve Statistics** (`GET /shorturls/<shortcode>`)  
  - Returns total clicks, click metadata, original URL, created/expiry timestamps.  
- **Error Handling**: Handles malformed inputs, expired/non-existent shortcodes, and invalid methods with descriptive JSON responses.  
- **Robust Code Quality**: Clear structure, modular components, error handling, and thread safety for URL storage.

---

## 🏗️ Architecture

   [ Client (Postman/Browser) ]
               |
               v
       +----------------+
       |   Flask App    |
       |    (app.py)    |
       +----------------+
               |
   -------------------------------
   |                             |
   v                             v
+-----------+             +----------------+
|  Logger   |             |   URL Store    |
| (logger)  |             | (url_store.py) |
+-----------+             +----------------+
                               |
                               v
                        [ Short URLs + Analytics ]


---

## 🚀 API Endpoints

### 1. Create Short URL
**POST** `/shorturls`

**Request Body:**
```json
{
  "url": "https://example.com/very/long/path",
  "validity": 45,
  "shortcode": "custom123"
}


**Response Created**


{
  "shortLink": "http://localhost:5000/custom123",
  "expiry": "2025-01-01T00:30:00Z"
}

Redirect to Original URL

GET /<shortcode>

Redirects to the original long URL.
If expired or invalid → returns JSON error.

3. Retrieve Short URL Statistics

GET /shorturls/<shortcode>

Response (200 OK):
{
  "original_url": "https://example.com/very/long/path",
  "created_at": "2025-01-01T00:00:00Z",
  "expiry": "2025-01-01T00:30:00Z",
  "total_clicks": 5,
  "clicks": [
    {
      "timestamp": "2025-01-01T00:05:00Z",
      "source": "https://google.com",
      "geo": "IN"
    }
  ]
}

**How to Run Locally**
Clone the repository:
git clone https://github.com/<your-username>/affordmed-url-shortener.git
cd affordmed-url-shortener/backend-test-submission

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

Install dependencies:
pip install flask

Run the app:
python app.py

Access the service:
Base URL: http://localhost:5000/
Use Postman or curl to test endpoints.





