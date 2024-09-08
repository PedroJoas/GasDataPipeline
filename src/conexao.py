import os
from dotenv import load_dotenv
import msal
import requests
import webbrowser

class APIConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.APP_ID = os.getenv("APP_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        # Para contas de organizações use o commom, caso seja pessoal use consumers
        self.authority_url = 'https://login.microsoftonline.com/common' 
        self.base_url = 'https://graph.microsoft.com/v1.0/'
        self.scopes = ['User.Read', 'Files.ReadWrite']
        self.client_instance = msal.ConfidentialClientApplication(
            client_id=self.APP_ID,
            client_credential=self.CLIENT_SECRET,
            authority=self.authority_url
        )
        self.access_token = None

    def authenticate(self):
        authorization_request_url = self.client_instance.get_authorization_request_url(self.scopes)
        webbrowser.open(authorization_request_url, new=True)

    def acquire_access_token(self, code):
        result = self.client_instance.acquire_token_by_authorization_code(code, self.scopes)
        if "access_token" in result:
            self.access_token = result['access_token']
            return self.access_token
        else:
            raise ValueError(f"Error acquiring token: {result.get('error_description')}")

    def make_graph_request(self, endpoint):
        if not self.access_token:
            raise ValueError("Access token is not available. Please authenticate first.")
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        return response.json()


