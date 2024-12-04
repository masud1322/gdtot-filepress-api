from flask import Flask, request, jsonify
from services.filepress import FilePressService
from services.gdtot import GDTOTService
import re

app = Flask(__name__)

filepress_service = FilePressService()
gdtot_service = GDTOTService()

def extract_drive_link(url):
    """Extract clean drive link from URL parameters"""
    patterns = [
        r'https://drive\.google\.com/\S+',
        r'drive\.google\.com/\S+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(0)
    return url

@app.route('/')
def home():
    try:
        return jsonify({
            "status": "success",
            "message": "API is working!",
            "endpoints": {
                "/f/[drive_link]": "Convert to FilePress link",
                "/gt/[drive_link]": "Convert to GDTOT link"
            },
            "example": {
                "filepress": "/f/https://drive.google.com/file/d/YOUR_FILE_ID/view",
                "gdtot": "/gt/https://drive.google.com/file/d/YOUR_FILE_ID/view"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/f/<path:drive_link>')
def filepress_convert(drive_link):
    try:
        clean_link = extract_drive_link(drive_link)
        result = filepress_service.convert_link(clean_link)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "filepress"
        }), 500

@app.route('/gt/<path:drive_link>')
def gdtot_convert(drive_link):
    try:
        clean_link = extract_drive_link(drive_link)
        gdtot_result = gdtot_service.convert_link(clean_link)
        
        if gdtot_result.get('success'):
            return jsonify({
                "success": True,
                "link": gdtot_result['link'],
                "service": "gdtot"
            })
        
        return jsonify({
            "success": False,
            "error": gdtot_result.get('error', 'Unknown error'),
            "service": "gdtot"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "gdtot"
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 