import requests

# sends request and output something like this:---Request begin---72
def send_request(url):
    try:
        response = requests.get(url)
        print(f"---Request begin---")
        print(f"{response.request.method} {response.request.url} HTTP/1.1")
        for header, value in response.request.headers.items():
            print(f"{header}: {value}")
        print()
        print(f"---Request end---")
        print(f"HTTP request sent, awaiting response...")
        print()
        print(f"---Response header ---")
        print(f"HTTP/{response.raw.version/10} {response.status_code} {response.reason}")
        for header, value in response.headers.items():
            if header.lower() == 'set-cookie':
                print(f"{header}: {value}")
            else:
                print(f"{header}: {value}")
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None