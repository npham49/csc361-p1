from urllib.parse import urlparse

def parse_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed = urlparse(url)
    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port or (443 if scheme == 'https' else 80)
    path = parsed.path or '/'
    
    # For google.com, try HTTPS first if HTTP was specified
    if scheme == 'http' and 'google' in host.lower():
        print(f"Trying HTTPS for {host} instead of HTTP")
        scheme = 'https'
        port = 443
    
    return scheme, host, port, path