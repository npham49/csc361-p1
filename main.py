import sys
from modules.http_client import send_request

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Testing URL: {url}")
        
        # Send request - this will handle all the parsing, connection, and printing
        result = send_request(url)
        if result:
            print("\nRequest completed successfully!")
        else:
            print("\nRequest failed.")
    else:
        print("Usage: python main.py <URL>")

if __name__ == "__main__":
    main()
