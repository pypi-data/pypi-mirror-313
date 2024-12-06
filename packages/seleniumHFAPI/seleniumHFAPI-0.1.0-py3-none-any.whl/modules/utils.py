import re
import unicodedata

import requests

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)  # Save the image as bytes
        print(f"Image saved to {save_path}")
    else:
        raise Exception("Failed to download image, status code:", response.status_code)


def sanitize_string(input_string, max_length=64):
    # Remove or replace unsafe characters
    safe_string = re.sub(r'[<>:"/\\|?*]', '', input_string)
    
    # Replace spaces with underscores
    safe_string = safe_string.replace(' ', '_')
    
    # Remove any non-ASCII characters
    safe_string = unicodedata.normalize('NFKD', safe_string).encode('ASCII', 'ignore').decode('ASCII')
    
    # Remove any remaining unsafe characters
    safe_string = re.sub(r'[^\w\-_.]', '', safe_string)
    
    # Truncate to the specified maximum length
    safe_string = safe_string[:max_length]
    
    # Remove any trailing periods or spaces
    safe_string = safe_string.rstrip('.').rstrip()
    
    # If the string is empty after sanitization, return a default name
    if not safe_string:
        return "untitled"
    
    return safe_string