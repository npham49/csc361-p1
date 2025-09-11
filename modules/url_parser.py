from urllib.parse import urlparse, parse_qs

# parses the proided URL, find and return the domain name (host)
#  values can come as http://www.example.com, https://example.com, example.com, www.example.com
def parse_url(url):
    
    # create and differenticate URL due to sometimes missing http/https
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed_url = urlparse(url)
    # check for errorneous URL
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL", url)
    host = parsed_url.netloc
    return host, url