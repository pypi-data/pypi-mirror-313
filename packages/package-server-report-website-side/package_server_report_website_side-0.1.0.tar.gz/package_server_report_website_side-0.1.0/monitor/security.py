import ssl
import socket
import requests

def get_ssl_certificate(url):
    try:
        host = url.split("://")[-1].split("/")[0]
        cert = ssl.get_server_certificate((host, 443))
        return {"ssl_certificate_status": "Valid"}
    except Exception as e:
        return {"ssl_certificate_status": "Invalid", "error": str(e)}

def get_http_headers(url):
    try:
        response = requests.head(url)
        return response.headers
    except Exception as e:
        return {"error": str(e)}
