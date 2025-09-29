# WebTester

## Overview

WebTester is a simple HTTP in Python client that collects information regarding a web server, this includes:

- Whether a server supports HTTP 2.0
- The cookies that a server sets
- Whether it is password protected

## Running the tester

### Prerequisites

- Python 3.x installed on your machine

### Steps

Run the following command in your terminal:

```bash
python3 WebTester.py <URL>
```

or if you have Python 3 as the default python interpreter:

```bash
python WebTester.py <URL>
```

If your Python 3 interpreter is named differently, adjust the command accordingly (e.g., `python` or `python3.8`).

Where URL can be any valid HTTP or HTTPS URL, for example:

```bash
python3 WebTester.py http://example.com
```

or

```bash
python3 WebTester.py example.com
```

## Architecture:

The project is structured into several modules, each has a set of functions to handle tasks related to that module. The aim of this architecture is to simulate Python code in a modular way, similar to how libraries like `requests` would be structured. The following modules are included:

- `http_client.py`: Handles the HTTP/HTTPS connection, request sending, and response receiving.
- `url_parser.py`: Parses the provided URL to extract components like scheme, host, port, and path.
- `final_tests.py`: Tests if the server supports HTTP 2.0, and verifies if the site is password protected.
- `response_analyzer.py`: Analyzes the HTTP response to extract cookies and print out relevant information like how the assignment showed as examples.
- `cookie_parser.py`: Parses the `Set-Cookie` headers to extract cookie details.
- `WebTester.py`: The main script that ties everything together and runs the tests.

## How it works:

1. When the user runs `WebTester.py` with a URL, the URL is parsed and passed on to `main.py`.
2. `main.py` uses send_request from `http_client.py`, this basically creates a socket connection to the server using `socket` and `ssl` libraries. This uses the scheme, host, port, path parsed from the URL to then construct an HTTP 1.1 GET request. In the case that SSL is needed (it's HTTPS), it wraps the socket with the SSL context.
3. The request is sent to the server, and the response is received. The response is read in chunks until the headers are fully received. This is parsed to extract the status code and headers. All the headers is also passed to `response_analyzer.py` to extract cookies (this is done using `cookie_parser.py`, a RegEx is ran to extract all cookies from the `Set-Cookie` headers) and print out relevant information. If the status code is >300 and <400, it means it's a redirect, so it will follow the redirect by calling `send_request` again with the new URL recursively. The cookie information is also passed along to the next request if there are any cookies set.
4. After the response is received, `final_tests.py` is used to check if the server supports HTTP 2.0 by sending an HTTP 2.0 request to the final redirect URL. Another check that is done is with the status code, if it's 401 or 403 or has the `WWW-Authenticate` header, it means the site is password protected.
5. Finally, all information is returned to the `main.py` and printed out.

### Parsing the URL (`url_parser.py` module)

The URL is parsed using the `url_parser.py` module, which extracts the following components:

- **Scheme**: The protocol used (e.g., HTTP or HTTPS). Sometimes the user might not provide this, so we default to HTTPS.
- **Host**: The domain name or IP address of the server, this is provided by the user as a parameter.
- **Port**: The port number to connect to (default is 80 for HTTP and 443 for HTTPS).
- **Path**: The specific resource being requested.

### Cookie parsing (`cookie_parser.py` module)

Cookies are parsed using a regular expression to handle the complexity of cookie strings, especially when attributes like `Expires` contain commas. The RegEx used is `,\s*(?=[a-zA-Z][a-zA-Z0-9_]*\s*=)`, which effectively splits cookies at commas that are followed by a valid cookie name and equals sign, ensuring that commas within attribute values do not cause incorrect splits.

The cookie object generated per cookie contains the following attributes:

- **original_string**: The original cookie string as received from the server.
- **subvalues**: A list of key-value pairs representing the cookie's attributes. (with `name` and `value` being the values)

### HTTP 2.0 and Password Protection Check (`final_tests.py` module)

To check if a server supports HTTP 2.0, an HTTP 2.0 request is sent to the server using the `http_client.py` module. If the server responds appropriately, it indicates support for HTTP 2.0. Another check that is done is with the status code, if it's 401 or 403 or has the `WWW-Authenticate` header, it means the site is password protected.

HTTP 2.0 requests are sent using:

```python
# Create SSL context with ALPN for HTTP/2 testing
context = ssl.create_default_context()
context.check_hostname = False
context.set_alpn_protocols(['h2', 'http/1.1'])
```

This was covered in one of the tutorials.

## LLM Usage

This is covered in [LLM.md](LLM.md)
