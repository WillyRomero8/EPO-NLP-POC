from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

def set_env_variables():
    load_dotenv()

    client_id = os.environ['AZURE_CLIENT_ID']
    tenant_id = os.environ['AZURE_TENANT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']
    vault_url = os.environ['AZURE_VAULT_URL']


    credentials = ClientSecretCredential(
        client_id = client_id,
        client_secret = client_secret,
        tenant_id = tenant_id
    )

    secret_client = SecretClient(vault_url = vault_url, credential = credentials)

    OPENAI_API_VERSION = secret_client.get_secret("OpenAI-api-version").value
    AZURE_OPENAI_ENDPOINT = secret_client.get_secret("OpenAI-endpoint").value
    AZURE_OPENAI_API_KEY = secret_client.get_secret("OpenAI-api-token").value

    os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
    os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY