from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_PATH = "silent-vim-443809-s8-7ce6d6590575.json"

try:
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    service = build("vision", "v1", credentials=credentials)
    print("✅ Google Vision API is authenticated!")
except Exception as e:
    print(f"❌ Authentication Error: {e}")
