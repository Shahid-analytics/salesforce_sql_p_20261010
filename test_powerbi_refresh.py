
import os
import msal
import requests
from dotenv import load_dotenv

load_dotenv()

tenant_id = os.getenv("POWERBI_TENANT_ID")
client_id = os.getenv("POWERBI_CLIENT_ID")
client_secret = os.getenv("POWERBI_CLIENT_SECRET")

workspace_id = "65f68826-e1c2-477e-9abc-2abefee0c5dd"
dataset_id = "291aff46-560d-4350-9ad3-8928264a7846"

# Authenticate with Microsoft Entra
app = msal.ConfidentialClientApplication(
    client_id=client_id,
    authority=f"https://login.microsoftonline.com/{tenant_id}",
    client_credential=client_secret,
)

token_result = app.acquire_token_for_client(
    scopes=["https://analysis.windows.net/powerbi/api/.default"]
)

if "access_token" not in token_result:
    raise RuntimeError(
        f"Authentication failed: {token_result.get('error_description')}"
    )

access_token = token_result["access_token"]

# Request a semantic model refresh
url = (
    f"https://api.powerbi.com/v1.0/myorg/groups/"
    f"{workspace_id}/datasets/{dataset_id}/refreshes"
)

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    },
    json={"notifyOption": "NoNotification"},
    timeout=30,
)

print("HTTP status:", response.status_code)

if response.status_code == 202:
    print("SUCCESS: Power BI accepted the refresh request.")
    print("Note: The refresh runs asynchronously; check its status in Power BI.")
else:
    print("Refresh request failed.")
    print("Response:", response.text)
