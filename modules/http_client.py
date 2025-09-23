import socket
import ssl
import modules.url_parser as url_parser
import modules.response_analyzer as response_analyzer
import modules.url_parser as url_parser
import modules.response_analyzer as response_analyzer


def create_connection(host, port, use_ssl=False):
    print(f"Connecting to {host}:{port} (SSL: {use_ssl})")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((host, port))
        print(f"Connected successfully to {host}:{port}")
        
        if use_ssl:
            context = ssl.create_default_context()
            # Disable cert verification like in reference
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=host)
            print("SSL handshake completed")
        
        return sock
    except Exception as e:
        sock.close()
        raise Exception(f"Connection failed to {host}:{port} - {e}")


def build_http_request(method, path, host, port, scheme):
    # Determine if we need port in Host header
    host_header = host
    if (scheme == 'http' and port != 80) or (scheme == 'https' and port != 443):
        host_header = f"{host}:{port}"
    
    # Simplified request - just the essentials that work
    request_lines = [
        f"{method} {path} HTTP/1.1",
        f"Host: {host_header}",
        "Connection: close",
        "",  # Empty line ends headers
        ""   # Extra empty line to ensure proper termination
    ]
    
    request_string = "\r\n".join(request_lines)
    
    # Store headers for printing
    headers_dict = {
        'Host': host_header,
        'Connection': 'close'
    }
    
    # Print actual request with proper newlines
    print("Built request:")
    for line in request_lines[:-1]:  # Don't print the last empty line
        if line:
            print(line)
    print()  # Empty line at end
    
    return request_string, headers_dict


def send_request_data(sock, request_string):
    print(f"Sending request ({len(request_string)} bytes)")
    # Use sendall to ensure all data is sent
    sock.sendall(request_string.encode('utf-8'))
    print(f"Sent all {len(request_string)} bytes successfully")


def receive_response(sock):
    response_data = b""
    
    print("Waiting for response...")
    
    # Set a timeout for receiving data
    sock.settimeout(10)
    
    try:
        # Receive data until we get complete headers (\r\n\r\n) or timeout
        header_end_found = False
        max_attempts = 50  # Prevent infinite loop
        attempts = 0
        
        while not header_end_found and attempts < max_attempts:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    print("Server closed connection")
                    break
                    
                response_data += chunk
                print(f"Received {len(chunk)} bytes (total: {len(response_data)})")
                
                # Check if we have complete headers
                if b'\r\n\r\n' in response_data:
                    header_end_found = True
                    print("Complete headers received")
                    break
                    
                attempts += 1
                
            except socket.timeout:
                print("Timeout waiting for more data")
                break
                
        # Remove timeout
        sock.settimeout(None)
        
    except Exception as e:
        print(f"Error receiving data: {e}")
        sock.settimeout(None)
    
    print(f"Total received: {len(response_data)} bytes")
    
    # Check if we got any data
    if not response_data:
        raise Exception("No response data received")
    
    # If we don't have complete headers, just work with what we have
    if b'\r\n\r\n' not in response_data:
        print("Warning: Incomplete headers, working with partial data")
        # Try to find at least one CRLF to separate status from potential headers
        if b'\r\n' in response_data:
            response_text = response_data.decode('utf-8', errors='ignore')
            lines = response_text.split('\r\n')
            if lines and lines[0]:
                # We have at least a status line
                status_line = lines[0]
                headers_part = '\r\n'.join(lines[1:]) if len(lines) > 1 else ""
                body = ""
            else:
                raise Exception("Invalid response format")
        else:
            raise Exception("No valid HTTP response headers found")
    else:
        # Normal case - we have complete headers
        response_text = response_data.decode('utf-8', errors='ignore')
        if '\r\n\r\n' in response_text:
            headers_part, body = response_text.split('\r\n\r\n', 1)
        else:
            headers_part = response_text
            body = ""
        
        lines = headers_part.split('\r\n')
        if not lines or not lines[0]:
            raise Exception("Invalid HTTP response: no status line")
        status_line = lines[0]
    
    # Extract status code and reason - with error checking
    parts = status_line.split(' ', 2)
    if len(parts) < 2:
        raise Exception(f"Invalid status line: {status_line}")
    
    try:
        status_code = int(parts[1])
    except ValueError:
        raise Exception(f"Invalid status code in: {status_line}")
    
    reason = parts[2] if len(parts) > 2 else ""
    
    # Parse headers into dictionary, handling multiple values for same header
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            name, value = line.split(':', 1)
            name = name.strip()
            value = value.strip()
            
            # Handle multiple headers with same name (like Set-Cookie)
            if name in headers:
                # Convert to list if not already
                if not isinstance(headers[name], list):
                    headers[name] = [headers[name]]
                headers[name].append(value)
            else:
                headers[name] = value
    
    return status_code, reason, headers, body


def send_request(url):
    try:
        # Step 1: Parse URL using url_parser

        scheme, host, port, path = url_parser.parse_url(url)
        
        use_ssl = (scheme == 'https')
        
        # Step 2: Create connection
        sock = create_connection(host, port, use_ssl)
        
        try:
            request_string, request_headers = build_http_request('GET', path, host, port, scheme)
            
            send_request_data(sock, request_string)
            
            status_code, reason, headers, body = receive_response(sock)
            
            response_analyzer.analyze_and_print_response(
                'GET', f"{scheme}://{host}:{port}{path}", 
                request_headers, status_code, reason, headers, body
            )
            
            # Handle redirects
            redirect_count = 0
            while 300 <= status_code < 400 and redirect_count < 5:
                redirect_url = headers.get('Location')
                if not redirect_url:
                    break
                
                print(f"\nFollowing redirect to {redirect_url}")
                sock.close()
                
                # Recursive call for redirect
                return send_request(redirect_url)
            
            # Return response data
            return {
                'status_code': status_code,
                'headers': headers,
                'body': body,
                'url': f"{scheme}://{host}:{port}{path}"
            }
            
        finally:
            sock.close()
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None