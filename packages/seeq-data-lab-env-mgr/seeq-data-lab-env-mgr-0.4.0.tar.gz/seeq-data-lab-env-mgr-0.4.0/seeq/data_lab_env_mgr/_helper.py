import re
from urllib.parse import urljoin
import requests
import time
from functools import wraps

APP_JS_PATTERN = r'/(assets|js)/app[^"]*\.js'
TOKEN_PATTERN = r'\.init\("([^"]+)",\s*\{[^}]*api_host:"https?://([^"]+)"'

def _extract_token_from_host(host):
    try:
        with requests.Session() as session:
            index_response = session.get(host)
            index_response.raise_for_status()
            
            app_js_paths = re.finditer(APP_JS_PATTERN, index_response.text)
            if not app_js_paths:
                raise Exception("No match for app.js")
            token_match = None
            for app_js in app_js_paths:
                app_js_url = urljoin(host, app_js.group(0))
                app_js_response = session.get(app_js_url)
                app_js_response.raise_for_status()
                token_match = re.search(TOKEN_PATTERN, app_js_response.text)
                if token_match:
                    break
            if not token_match:
                raise Exception("No match for token")
            return token_match.group(1), token_match.group(2)
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None, None

def rate_limit(interval_seconds):
    def decorator(func):
        last_call_time = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            now = time.time()
            if func not in last_call_time or (now - last_call_time[func]) > interval_seconds:
                last_call_time[func] = now
                return func(*args, **kwargs)

        return wrapper
    return decorator