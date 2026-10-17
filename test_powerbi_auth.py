
import os
import msal
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()

tenant_id = os.getenv("POWERBI_TENANT_ID")
client_id = os.getenv("POWERBI_CLIENT_ID")
client_secret = os.getenv("POWERBI_CLIENT_SECRET")

# Check that all required credentials exist
if not all([tenant_id, client_id, client_secret]):
    raise ValueError(
        "Missing Power BI credentials. Check your .env file."
    )

# Create an application for Microsoft authentication
app = msal.ConfidentialClientApplication(
    client_id=client_id,
    authority=f"https://login.microsoftonline.com/{tenant_id}",
    client_credential=client_secret,
)

# Request an access token for Power BI
result = app.acquire_token_for_client(
    scopes=["https://analysis.windows.net/powerbi/api/.default"]
)

if "access_token" in result:
    print("SUCCESS: Microsoft authentication completed.")
    print("An access token was received.")
else:
    print("FAILED: Microsoft authentication failed.")
    print("Error:", result.get("error"))
    print("Description:", result.get("error_description"))
