import base64
import json
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from apps.core.managers.email import EmailManager

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send"]


class GoogleEmailManager(EmailManager):
    __service = None

    def init_connection(self, project_id, client_id, client_secret):
        creds = None
        filepath = "share/token.pickle"
        if os.path.exists(filepath):
            with open(filepath, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                self.__generate_client_file(project_id, client_id, client_secret)
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=58336)
            with open(filepath, "wb") as token:
                pickle.dump(creds, token)
        self.__service = build("gmail", "v1", credentials=creds)
        return self.__service

    def __generate_client_file(self, project_id, client_id, client_secret):
        client_data = {
            "web": {
                "client_id": client_id,
                "project_id": project_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost:58336/"],
                "javascript_origins": ["http://localhost:8000"],
            }
        }
        json.dump(client_data, open("credentials.json", "w"))

    def _send_email(self, origin, to, content, **xtra_args):
        b64_bytes = base64.urlsafe_b64encode(content.as_bytes())
        b64_string = b64_bytes.decode()
        content = {"raw": b64_string}
        response = self.__service.users().messages().send(userId="me", body=content).execute()
        return response
