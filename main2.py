import webbrowser
import msal
from msal import PublicClientApplication
import requests
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("APP_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
authority_url = 'https://login.microsoftonline.com/common'
base_url = 'https://graph.microsoft.com/v1.0/'

scopes = ['User.Read', 'Files.ReadWrite']

# metodo 1: autorizacao com codigo de autorizacao
client_instance = msal.ConfidentialClientApplication(
    client_id=APP_ID,
    client_credential=CLIENT_SECRET,
    authority = authority_url
)
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'  # Caminho para o Chrome no macOS

authorization_request_url = client_instance.get_authorization_request_url(scopes)

print(authorization_request_url)
webbrowser.get(chrome_path).open(authorization_request_url,new=True)

# Automatizo usando requests e pego o parametro code 
authorization_code = '0.AQoAVK6RtcIziUW-ZpAhpBlsfN3eE7qbv_lHq6Snh3u9iggKANE.AgABBAIAAAApTwJmzXqdR4BN2miheQMYAwDs_wUA9P9Ji_BYZ8MDRLPoONOCX150dOiMSOuyEwbzyvDEy8XhlifKf_WH0_18Il1EvscLkElf9uuBgi8g2LX8w6J1sRV13Fp9FsQnMbY7WDFvggLsozNNN1AFdwKNyXq6m7NX13deYHydcg5o8qkYaNgDs4qj8ezPRBUjIieGrYh9xIMcPEKUMLCHRIHIoM62xJTY2f56YxDw1BSZQjCR7Sr1a2p329ndea7HufpNBL9zqpJ4aIzRbhoeWEK0d1ejIjOBJQk2KpJtRVJhvE-UkC85lOf3hxTSJVURYmBN6_1nPrSl_D2M3VaFQ0gU_VbDIB7yoj3OmYImGzDVeUiD1f4hNWKsgqUiC06tXysLOyynZJbSz17YV-2dZUVLxzoFDp6RjF-nlQLFUMlOtum5y2XrAZbxmFKqFhEVNrJDqw7Cdwwh4F1soex_dhUJcT4B0ke4eMrkmqvf58Zlh66LbdqqMO0WB7dl9ZPONbvyurPuFUtY2VcqYR2WlgGNZmltYlFyblcm_naMgLn-VZY3RHTThjMo4eogwexhYzpUQOPnw43lFO8ei0jR15AFCpE9iZagl3FdOxztC9RhbKKSxMg4OOcoFRzCUKEUgo6einl-Fpg21Lh4DqiqW_nJqTORQHKe8akIfbf3pGH_ZDv15K_rLrFay8SNI6ejwDOUFJJWxei2oqYOMuvvXqFps-YpaZi7qN5egn5x71GE46V0aSIYjG5ELBKX48k'

acess_token = client_instance.acquire_token_by_authorization_code(
    code=authorization_code,
    scopes=scopes
)

print(acess_token['acess_token'])