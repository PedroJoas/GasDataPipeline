import os
from dotenv import load_dotenv
import msal
import requests
import webbrowser
from requests.exceptions import RequestException

class APIConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.APP_ID = os.getenv("APP_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.USER_ID = os.getenv("USER_ID")
        self.DRIVE_ID = os.getenv("DRIVE_ID")
        # Para contas de organizações use o commom, caso seja pessoal use consumers
        self.authority_url = 'https://login.microsoftonline.com/common' 
        self.base_url = 'https://graph.microsoft.com/v1.0/me/'
        self.scopes = ['User.Read', 'Files.ReadWrite']
        self.client_instance = msal.ConfidentialClientApplication(
            client_id=self.APP_ID,
            client_credential=self.CLIENT_SECRET,
            authority=self.authority_url
        )
        self.access_token = None

    def authenticate(self) -> None:
        authorization_request_url = self.client_instance.get_authorization_request_url(self.scopes)
        webbrowser.open(authorization_request_url, new=True)

    def acquire_access_token(self, code:str) -> str:
        result = self.client_instance.acquire_token_by_authorization_code(code, self.scopes)
        if "access_token" in result:
            self.access_token = result['access_token']
            return self.access_token
        else:
            raise ValueError(f"Error acquiring token: {result.get('error_description')}")

    def _make_graph_request(self, endpoint:str, request:str = 'GET', data=None):
        if not self.access_token:
            raise ValueError("Access token is not available. Please authenticate first.")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        if request == 'GET':
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        else:
            response = requests.post(f"{self.base_url}{endpoint}", headers=headers)

        if response.status_code in range(200, 300):
            return response.json()
        else:
            raise Exception(f"Request failed: {response.status_code} - {response.text}")

    
    def mkdir(self):
        
        pass
    
    def _find_dir(self, dirname: str) -> str:
        endpoint = 'https://graph.microsoft.com/v1.0/me/drive/root/children'

        try:
            response = self._make_graph_request(endpoint)
            for dir in response['value']:
                if dir['name'] == dirname:
                    return dir['id']
            raise Exception(f"Diretório não encontrado: {response.status_code} - {response.text}")
        
        except RequestException as err:
            print(f'Falha na requisição: {err}')

    def _upload_session(self, dirname:str, filename:str):
        
        item_id = self._find_dir(dirname)
        endpoint = f'/drives/{self.DRIVE_ID}/items/{item_id}/createUploadSession'
        request = 'POST'

        payload = {
            "item": {
                "@microsoft.graph.conflictBehavior": "replace",
                "name": f"{filename}.csv"
            }
        }

        return self._make_graph_request(endpoint, request, data=payload)

    def add_files(self):
        pass
    def search_files(self):
        endpoint = ''
        pass

    def download_files(self):
        endpoint = ''
        pass



