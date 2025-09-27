from modules.cookie_parser import parse_cookies

def analyze_and_print_response(method, url, request_headers, status_code, reason, response_headers, body):
    # Print request
    print("---Request begin---")
    print(f"{method} {url}")
    for header, value in request_headers.items():
        print(f"{header}: {value}")
    print("---Request end---")
    print("HTTP request sent, awaiting response...")
    print()
    
    # Print response headers
    print("---Response header ---")
    print(f"{status_code} {reason}")
    
    # Handle Set-Cookie headers specially
    set_cookie_values = []
    for header, value in response_headers.items():
        if header.lower() == 'set-cookie':
            # Handle both single values and lists of values
            if isinstance(value, list):
                set_cookie_values.extend(value)
            else:
                set_cookie_values.append(value)
        else:
            # For non-cookie headers, handle lists by joining them
            if isinstance(value, list):
                print(f"{header}: {', '.join(value)}")
            else:
                print(f"{header}: {value}")
                
    final_cookies_list = []
    
    # Parse and print cookies using cookie_parser
    if set_cookie_values:
        for cookie_str in set_cookie_values:
            cookies = parse_cookies(cookie_str)
            
            final_cookies_list.extend(cookies)
            for cookie in cookies:
                print(f"Set-Cookie: {cookie['original_string']}")
    print()
    
    # Print response body
    print("--- Response body ---")
    print(body)
    
    print(f"length of cookies: {len(set_cookie_values)}")

    return final_cookies_list