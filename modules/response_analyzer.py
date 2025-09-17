from modules.cookie_parser import parse_cookies


def analyze_response(response):
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
            cookie_dict = parse_cookies(value)
            for cookie in cookie_dict:
                print(f"Set-Cookie: {cookie['original_string']}")
        else:
            print(f"{header}: {value}")
    print(f"--- Response body ---")
    print(f"{response.text}")