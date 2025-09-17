import requests

from modules.cookie_parser import parse_cookies
from modules.response_analyzer import analyze_response

# sends request and output something like this:---Request begin---72
def send_request(url):
    try:
        response = requests.get(url, allow_redirects=False)
        analyze_response(response)
        status_code = response.status_code
        
        # if the returned status code is 3xx, follow the redirect
        while 300 <= status_code < 400:
            redirect_url = response.headers.get('Location')
            
            if redirect_url:
                print(f"Following redirect to {redirect_url}")
                response = requests.get(redirect_url, allow_redirects=False)
                analyze_response(response)
                status_code = response.status_code
        if not (300 <= status_code < 400):
            return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None