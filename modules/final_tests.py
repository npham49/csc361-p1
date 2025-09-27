import socket
import ssl

def test_http2_support(scheme, host, port):
    try:
        
        # Only test HTTPS URLs (HTTP/2 over plain HTTP is rare)
        if scheme != 'https':
            print("HTTP/2 testing skipped - not HTTPS")
            return False
        
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Set timeout for HTTP/2 test
        
        try:
            sock.connect((host, port))
            
            # Create SSL context with ALPN for HTTP/2 testing
            context = ssl.create_default_context()
            context.check_hostname = False
            context.set_alpn_protocols(['h2', 'http/1.1'])
            
            # Wrap socket with SSL
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            
            # Check what protocol was negotiated
            if hasattr(ssl_sock, 'selected_alpn_protocol'):
                protocol = ssl_sock.selected_alpn_protocol()
                print(f"ALPN negotiated protocol: {protocol}")
                
                if protocol == 'h2':
                    print("Supports HTTP/2")
                    return True
                elif protocol == 'http/1.1':
                    print("Only supports HTTP/1.1")
                    return False
                else:
                    print(f"Unknown protocol {protocol}")
                    return False
            else:
                print("ALPN protocol information not available")
                return False
                
        finally:
            try:
                sock.close()
            except:
                pass
                
    except Exception as e:
        print(f"HTTP/2 test failed: {e}")
        return False


def check_password_protected(status_code, response_headers):
    if status_code == 401:
        return True
    
    if status_code == 403:
        return True
    
    www_authenticate = response_headers.get('WWW-Authenticate')
    if www_authenticate:
        return True
    
    return False