import requests
import time

def get_website_performance(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start_time
        return {
            "status_code": response.status_code,
            "response_time": load_time,
            "status": "Up" if response.status_code == 200 else "Down"
        }
    except requests.exceptions.RequestException as e:
        return {"status": "Down", "error": str(e)}
