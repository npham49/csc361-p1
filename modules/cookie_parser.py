import re

def parse_cookies(cookie_string):
    # Parse cookies and return an array of objects with original_string and subvalues
    if not cookie_string:
        return []
    
    # Split cookies using regex that handles commas in dates properly
    cookie_pattern = r',\s*(?=[a-zA-Z][a-zA-Z0-9_]*\s*=)'
    individual_cookies = re.split(cookie_pattern, cookie_string)
    
    result = []
    
    # Parse each cookie
    for cookie_str in individual_cookies:
        cookie_str = cookie_str.strip()
        if not cookie_str:
            continue
            
        # Split cookie into name=value and attributes
        parts = [part.strip() for part in cookie_str.split(';')]
        if not parts:
            continue
        
        # Create subvalues array
        subvalues = []
        
        # Parse each part (name=value pairs)
        for part in parts:
            if '=' in part:
                name, value = part.split('=', 1)
                subvalues.append({
                    'name': name.strip(),
                    'value': value.strip()
                })
            else:
                # Handle attributes without values (like 'secure', 'HttpOnly')
                subvalues.append({
                    'name': part.strip(),
                    'value': ''
                })
        
        # Create cookie object
        cookie_obj = {
            'original_string': cookie_str,
            'subvalues': subvalues
        }
        
        result.append(cookie_obj)
    
    return result