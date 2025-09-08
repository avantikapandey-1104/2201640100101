import threading
from datetime import datetime, timedelta
import random
import string

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.urls = {}  # shortcode -> url data

    def _generate_shortcode(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            shortcode = ''.join(random.choices(chars, k=length))
            if shortcode not in self.urls:
                return shortcode

    def cleanup_expired(self):
        with self.lock:
            now = datetime.utcnow()
            expired_keys = [code for code, data in self.urls.items() if data["expiry"] < now]
            for code in expired_keys:
                del self.urls[code]

    def add_url(self, original_url, validity_minutes=30, custom_shortcode=None):
        with self.lock:
            self.cleanup_expired()
            if custom_shortcode:
                if custom_shortcode in self.urls:
                    raise ValueError("Shortcode already exists")
                shortcode = custom_shortcode
            else:
                shortcode = self._generate_shortcode()

            expiry = datetime.utcnow() + timedelta(minutes=validity_minutes)
            self.urls[shortcode] = {
                "original_url": original_url,
                "created_at": datetime.utcnow(),
                "expiry": expiry,
                "clicks": [],
                "total_clicks": 0
            }
            return shortcode, expiry

    def get_url(self, shortcode):
        with self.lock:
            self.cleanup_expired()
            data = self.urls.get(shortcode)
            if not data:
                return None
            return data

    def record_click(self, shortcode, source=None, geo=None):
        with self.lock:
            data = self.urls.get(shortcode)
            if not data:
                return False
            click_info = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": source,
                "geo": geo
            }
            data["clicks"].append(click_info)
            data["total_clicks"] += 1
            return True

    def get_stats(self, shortcode):
        with self.lock:
            self.cleanup_expired()
            data = self.urls.get(shortcode)
            if not data:
                return None
            return {
                "original_url": data["original_url"],
                "created_at": data["created_at"].isoformat() + "Z",
                "expiry": data["expiry"].isoformat() + "Z",
                "total_clicks": data["total_clicks"],
                "clicks": data["clicks"]
            }

url_store = URLStore()
