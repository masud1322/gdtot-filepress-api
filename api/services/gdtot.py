import requests
import re
import json
from bs4 import BeautifulSoup
from .config import config

class GDTOTService:
    def __init__(self):
        self.config = config["gdtot"]
        self.domain = self.config["domain"]
        self.cookies = self.config["cookies"]
    
    def convert_link(self, drive_link):
        """Convert Google Drive link to GDTOT link"""
        try:
            session = requests.Session()
            
            # Debug cookies
            print("\nCookies Debug:")
            print(f"Config Cookies: {self.cookies}")
            print(f"Crypt Value: {self.cookies['crypt']}")
            
            # First load upload-link page
            upload_url = f"{self.domain}/upload-link"
            initial_response = session.get(
                upload_url, 
                cookies={"crypt": self.cookies["crypt"]},
                timeout=30
            )
            
            print(f"Initial Response Status: {initial_response.status_code}")
            print(f"Session Cookies: {session.cookies.get_dict()}")
            
            # API রিকোয়েস্ট
            api_url = f"{self.domain}/ajax.php?ajax=upload-link"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.domain,
                "Referer": f"{self.domain}/upload-link",
                "X-Requested-With": "XMLHttpRequest"
            }
            
            # ড্রাইভ লিংক ফরম্যাট চেক
            if 'drive.google.com' in drive_link:
                # ID এক্সট্র্যাক্ট করি
                file_id = re.search(r'[-\w]{25,}', drive_link)
                if file_id:
                    # যদি uc ফরম্যাটে থাকে তবে সেটাই ব্যবহার করব
                    if 'uc?id=' in drive_link:
                        drive_link = f'https://drive.google.com/uc?id={file_id.group(0)}&export=download'
                    else:
                        drive_link = f'https://drive.google.com/file/d/{file_id.group(0)}/view'
            
            data = {
                "url": drive_link,
                "ajax": "upload-link"
            }
            
            print("\nRequest Info:")
            print(f"Drive Link: {drive_link}")
            print(f"Cookies: {session.cookies.get_dict()}")
            
            response = session.post(
                api_url,
                headers=headers,
                data=data,
                cookies=self.cookies,
                timeout=30
            )
            
            print(f"\nResponse Info:")
            print(f"Status: {response.status_code}")
            print(f"Response Text: {response.text[:500]}")
            
            if response.status_code == 200:
                # Try to find the link in different formats
                link_patterns = [
                    r'https://new7\.gdtot\.dad/file/\d+',
                    r'https://gdtot\.dad/file/\d+',
                    r'class="btn btn-primary".+?href="(.+?)"'
                ]
                
                for pattern in link_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        gdtot_link = match.group(1) if 'href' in pattern else match.group(0)
                        
                        # Get file info
                        soup = BeautifulSoup(response.text, 'html.parser')
                        file_info = soup.find('div', {'class': ['filename', 'file-name']})
                        size_info = soup.find('div', {'class': ['filesize', 'file-size']})
                        
                        return {
                            "success": True,
                            "link": gdtot_link,
                            "service": "gdtot",
                            "details": {
                                "name": file_info.text.strip() if file_info else "Unknown",
                                "size": size_info.text.strip() if size_info else "Unknown"
                            }
                        }
            
            return {
                "success": False,
                "error": "Could not generate GDTOT link. Please check your cookies.",
                "service": "gdtot"
            }
            
        except Exception as e:
            print(f"GDTOT Error: {str(e)}")
            return {
                "success": False,
                "error": f"GDTOT Error: {str(e)}",
                "service": "gdtot"
            } 