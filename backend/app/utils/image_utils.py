import base64
import os
import uuid
import uuid
from flask import current_app

def save_base64_image(base64_string: str) -> str:
    """
    Decodes a base64 string, saves it to static/uploads, and returns the public URL.
    Returns None if decoding fails or string is empty.
    """
    if not base64_string:
        return None

    try:
        # Check if the string contains a data URL prefix and remove it
        if "," in base64_string:
            header, base64_string = base64_string.split(",", 1)
        
        image_data = base64.b64decode(base64_string)
        
        # Generate a unique filename
        filename = f"pet_{uuid.uuid4().hex}.jpg"
        
        # Path to static folder
        static_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(static_folder, exist_ok=True)
        
        file_path = os.path.join(static_folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(image_data)
            
        return f"/static/uploads/{filename}"
    except Exception as e:
        print(f"Error decoding base64 image: {e}")
        return None
