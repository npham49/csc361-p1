import sys

from modules import url_parser
from modules import http_client

def main():
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        print(f"First argument: {first_arg}")

        # Call the URL parser and print the host
        host, parsed_url = url_parser.parse_url(first_arg)
        print(f"Host: {host}")
        
        # send request to host
        status_code = http_client.send_request(parsed_url)
        if status_code is not None:
            print(f"Response Status Code: {status_code}")
        else:
            print("Failed to get a response.")
    else:
        print("No arguments provided")

if __name__ == "__main__":
    main()
