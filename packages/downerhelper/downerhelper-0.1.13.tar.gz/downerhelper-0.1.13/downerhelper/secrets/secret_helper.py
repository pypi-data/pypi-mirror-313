from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import logging

def get_secret_value(secret_name, vault_url, queue=None, credential=DefaultAzureCredential()):
    try:
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        message = f"Error getting secret {secret_name}: {e}"
        if queue != None:
            queue.add('ERROR', message)
        else:
            logging.error(message)
    return None

def get_config_dict(secret_name, keyvault_url, dbname=None):
    db_config_str = get_secret_value(secret_name, keyvault_url)
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    config = {k: v for k, v in zip(keys, db_config_split)}
    if dbname != None: config['dbname'] = dbname
    return config

def get_key_url(secret_name, keyvault_url, queue=None):
    try:
        value = get_secret_value(secret_name, keyvault_url)
        index = value.find('/')
        return value[:index], value[index+1:]
    except Exception as e:
        message = f"Error getting key URL {secret_name}: {e}"
        if queue != None:
            queue.add('ERROR', message)
        else:
            logging.error(message)
        # queue.add('ERROR', f"Error getting key URL {secret_name}: {e}")
        raise e
    
def form_connection_string(storage_account, storage_account_key):
    return f"DefaultEndpointsProtocol=https;AccountName={storage_account};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"