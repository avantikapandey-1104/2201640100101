from flask import Flask, request, jsonify, redirect
import re
from logger import logging_middleware, logger
from url_store import url_store

app = Flask(__name__)
logging_middleware(app)

SHORTCODE_REGEX = re.compile(r'^[a-zA-Z0-9]{4,20}$')

def error_response(message, status_code):
    response = jsonify({"error": message, "status": status_code})
    response.status_code = status_code
    return response

def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?://)'  # http:// or https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # domain
        r'(:\d+)?'  # optional port
        r'(/.*)?$'  # path
    )
    return url_regex.match(url) is not None


@app.route('/', methods=['GET'])
def root():
    return {
        "message": "URL Shortener Microservice is running. Use /shorturls endpoint to create short URLs."
    }


@app.route('/shorturls', methods=['POST'])
def create_shorturl():
    data = request.get_json()
    if not data or 'url' not in data:
        return error_response("Missing 'url' in request body", 400)

    original_url = data['url']
    if not is_valid_url(original_url):
        return error_response("Invalid URL format", 400)

    validity = data.get('validity', 30)
    try:
        validity = int(validity)
        if validity <= 0:
            raise ValueError()
    except:
        return error_response("Invalid validity value", 400)

    shortcode = data.get('shortcode')
    if shortcode:
        if not SHORTCODE_REGEX.match(shortcode):
            return error_response("Invalid shortcode format. Must be alphanumeric and 4-20 chars", 400)

    try:
        shortcode, expiry = url_store.add_url(original_url, validity, shortcode)
    except ValueError as e:
        return error_response(str(e), 409)

    short_link = f"{request.host_url.rstrip('/')}/{shortcode}"
    return jsonify({
        "shortLink": short_link,
        "expiry": expiry.isoformat() + "Z"
    }), 201


@app.route('/shorturls/<string:shortcode>', methods=['GET'])
def get_shorturl_stats(shortcode):
    data = url_store.get_stats(shortcode)
    if not data:
        return error_response("Shortcode not found or expired", 404)
    return jsonify(data), 200


@app.route('/<string:shortcode>', methods=['GET'])
def redirect_shorturl(shortcode):
    data = url_store.get_url(shortcode)
    if not data:
        return error_response("Shortcode not found or expired", 404)

    # Record click with IP fallback
    source = request.headers.get('Referer')
    geo = request.headers.get('X-Geo-Location')
    if not geo:
        geo = request.remote_addr
    url_store.record_click(shortcode, source, geo)

    return redirect(data['original_url'], code=302)


# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return error_response("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("Method not allowed", 405)

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return error_response("Internal server error", 500)


if __name__ == '__main__':
    app.run(debug=True)
