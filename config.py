import os

# API Configuration
config = {
    # GDTOT Configuration
    "gdtot": {
        "domain": "https://new7.gdtot.dad",
        "cookies": {
            "crypt": "RFhObHFtMTBlclBQd2xaTXhzMVhsdG1jMVJaMnN6L0o3WndxcXBQMVExQT0%3D"
        }
    },
    
    # Simplified FilePress Configuration
    "filepress": {
        "domain": "https://new2.filepress.top",
        "api_key": "AVz7RiNiv29JlWFRgrsiPRbhfL4csJdQ"
    }
}

# Helper functions
def get_gdtot_config():
    return config["gdtot"]

def get_filepress_config():
    return config["filepress"] 