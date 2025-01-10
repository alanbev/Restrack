import os

# Remove trailing slash to prevent double slash issues
API_URL = os.getenv('API_URL', 'http://localhost:8000/api/v1').rstrip('/')
