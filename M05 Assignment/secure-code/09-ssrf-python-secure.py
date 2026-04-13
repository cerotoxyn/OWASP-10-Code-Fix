from urllib.parse import urlparse
import requests
import socket
import ipaddress

ALLOWED_HOSTS = {"api.example.com", "data.example.com"}

def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)

        if parsed.scheme != "https":
            return False

        host = parsed.hostname
        if not host or host not in ALLOWED_HOSTS:
            return False

        resolved_ip = ipaddress.ip_address(socket.gethostbyname(host))
        if (
            resolved_ip.is_private
            or resolved_ip.is_loopback
            or resolved_ip.is_link_local
            or resolved_ip.is_multicast
            or resolved_ip.is_reserved
        ):
            return False

        return True
    except Exception:
        return False

url = input("Enter URL: ").strip()

if not is_safe_url(url):
    print("Invalid or disallowed URL")
else:
    response = requests.get(url, timeout=5, allow_redirects=False)
    print(response.text)