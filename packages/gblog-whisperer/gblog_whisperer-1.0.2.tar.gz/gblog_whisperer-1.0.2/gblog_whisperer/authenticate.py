from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/blogger"]

def authenticate(client_secret_file, token_file="token.json"):
    """
    Authenticate with Blogger API using OAuth 2.0 and reuse the token to avoid repeated redirection.
    :param client_secret_file: Path to client secret JSON file.
    :param token_file: Path to the token file for storing and reusing credentials.
    :return: Authenticated Blogger service object.
    """
    creds = None

    # Check if the token file exists
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials are found, start the flow to generate them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)
