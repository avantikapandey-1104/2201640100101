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


