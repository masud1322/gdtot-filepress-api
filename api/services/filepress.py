import requests
import re
import json
from services.config import config

class FilePressService:
    def __init__(self):
        self.config = config["filepress"]
        self.domain = self.config["domain"]
        self.api_key = self.config["api_key"]
    
    def extract_drive_id(self, url):
        """Extract Drive ID from URL"""
        try:
            print(f"\nExtracting ID from URL: {url}")
            
            # For uc format links
            if 'uc?id=' in url:
                id_match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
                if id_match:
                    drive_id = id_match.group(1)
                    print(f"Found ID (uc format): {drive_id}")
                    return drive_id
            
            # For file/d/ format links
            if 'file/d/' in url:
                id_match = re.search(r'file/d/([a-zA-Z0-9_-]+)', url)
                if id_match:
                    drive_id = id_match.group(1)
                    print(f"Found ID (file/d format): {drive_id}")
                    return drive_id
            
            # For direct ID format
            id_match = re.search(r'[-\w]{25,}', url)
            if id_match:
                drive_id = id_match.group(0)
                print(f"Found ID (direct format): {drive_id}")
                return drive_id
            
            print("No valid Drive ID found in URL")
            return None
            
        except Exception as e:
            print(f"Error extracting Drive ID: {str(e)}")
            return None
    
    def convert_link(self, drive_link):
        """Convert Google Drive link to FilePress link"""
        try:
            drive_id = self.extract_drive_id(drive_link)
            if not drive_id:
                return {
                    "success": False,
                    "error": "Invalid Drive link format",
                    "service": "filepress"
                }
            
            # API endpoint
            api_url = f"{self.domain}/api/v1/file/add"
            
            # Headers with API key
            headers = {
                "Content-Type": "application/json"
            }
            
            # Payload with only API key and drive ID
            payload = {
                "key": self.api_key,  # Using the API key directly
                "id": drive_id
            }
            
            print("\nFilePress Request:")
            print(f"URL: {api_url}")
            print(f"Headers: {headers}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Make request
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print("\nFilePress Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"Parsed Response: {json.dumps(result, indent=2)}")
                    
                    if result.get("status") and result.get("data"):
                        file_id = result["data"].get("_id")
                        if file_id:
                            file_url = f"{self.domain}/file/{file_id}"
                            return {
                                "success": True,
                                "link": file_url,
                                "service": "filepress",
                                "details": {
                                    "name": result["data"].get("name", "Unknown"),
                                    "size": result["data"].get("size", "Unknown")
                                }
                            }
                    
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error"),
                        "service": "filepress"
                    }
                    
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "error": "Invalid JSON response",
                        "service": "filepress"
                    }
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", response.text)
                except:
                    error_msg = response.text
                
                return {
                    "success": False,
                    "error": f"API Error ({response.status_code}): {error_msg}",
                    "service": "filepress"
                }
                
        except Exception as e:
            print(f"\nError Details: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "service": "filepress"
            }
