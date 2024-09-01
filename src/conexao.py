from dotenv import load_dotenv
from google.cloud import bigquery, storage
import os

class Conexao:

    def __init__(self):
        load_dotenv()

        key = os.getenv('GOOGLE_APPLICATIONS_CREDENTIALS')

        self.client = storage.Client()

    def list_buckets(self):
        buckets = list(self.client.list_buckets())

        for bucket in buckets:
            print(bucket.name)
    
    def create_bucket(self):
        pass