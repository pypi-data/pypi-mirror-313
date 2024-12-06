from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def create_keyvault_client(keyvault_url):
    """
    Creates azure keyvault client based on vault url
    Parameters:
       keyvault_url (str): URL of azure keyvault
    Returns
        SecretClient: client created using url and DefaultAzureCredential
    """
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=keyvault_url, credential=credential)

        return client
    except Exception as err:
        raise Exception(f"Creating client failed: {err}")


def get_keyvault_secret(client, secret_name):
    """
    Retrieve a secret from azure keyvault

    Parameters:
        client (SecretClient): Azure secret client
        secret_name (str): Name of the secret being retrieved
    Returns:
        secret: The secret, or None if not found
    """
    try:
        secret = client.get_secret(secret_name)
        return secret
    except Exception as err:
        raise Exception(f"Query failed: {err}")
