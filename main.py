import sys
from modules.http_client import send_request

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Testing URL: {url}")
        
        # Send request - this will handle all the parsing, connection, and printing
        result = send_request(url)
        if result:
            # print out all results
            print(f"\nResults:")
            print(f"\nwebsite: {result['url']}")
            print(f"1. Supports http2: {result['support_http2']}")
            print(f"2. List of Cookies:")
            for cookie in result['cookies']:
                if cookie['subvalues']:
                    #  First one is always the main cookie name=value
                    cookie_name = cookie['subvalues'][0]['name']

                    remaining_subvalues = []
                    for subvalue in cookie['subvalues'][1:]:
                        if subvalue['value']:
                            remaining_subvalues.append(f"{subvalue['name']}:{subvalue['value']}")
                        else:
                            remaining_subvalues.append(subvalue['name'])
                    
                    if remaining_subvalues:
                        print(f"cookie name: {cookie_name}, {'; '.join(remaining_subvalues)}")
                    else:
                        print(f"cookie name: {cookie_name}")
            print(f"3. Password protected: {'yes' if result['password_protected'] else 'no'}")
        else:
            print("\nRequest failed.")
    else:
        print("Usage: python main.py <URL>")

if __name__ == "__main__":
    main()
