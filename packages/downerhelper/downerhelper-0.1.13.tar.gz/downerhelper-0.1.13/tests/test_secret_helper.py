import pytest
from downerhelper.secrets import get_secret_value, get_config_dict, get_key_url
from downerhelper.logs import setup_queue
import os 
import logging 
from uuid import uuid4

@pytest.fixture(scope="module")
def queue():
    return setup_queue('pytest', str(uuid4()), os.getenv('LOG_TABLE'), 'db-config-1', os.getenv('KEYVAULT_URL'))

def test_valid_secret_logging(queue):
    value = get_secret_value('test-secret', os.getenv('KEYVAULT_URL'))
    assert value == 'dfaec67d-cf0a-44e8-b5df-6e8346092450'

def test_valid_secret_logging(queue):
    value = get_secret_value('test-secret', os.getenv('KEYVAULT_URL'), queue)
    assert value == 'dfaec67d-cf0a-44e8-b5df-6e8346092450'

def test_invalid_secret(queue):
    value = get_secret_value('invalid', os.getenv('KEYVAULT_URL'), queue)
    assert value == None

def test_invalid_keyvault(queue):
    value = get_secret_value('test-secret', 'https://invalid.vault.azure.net', queue)
    assert value == None

def test_get_config_dict(queue):
    secret_name = 'db-config-test'
    db_config = get_config_dict(secret_name, os.getenv('KEYVAULT_URL'))
    assert db_config == {
        'dbname': 'value0',
        'user': 'value1',
        'password': 'VALue2',
        'host': 'value3'
    }

    altered_dbname = 'changed-dbname'
    db_config = get_config_dict(secret_name, os.getenv('KEYVAULT_URL'), altered_dbname)
    assert db_config == {
        'dbname': altered_dbname,
        'user': 'value1',
        'password': 'VALue2',
        'host': 'value3'
    }

    with pytest.raises(Exception):
        get_config_dict('invalid', os.getenv('KEYVAULT_URL'))

def test_get_key_url(queue):
    key, url = get_key_url('test-key-url', os.getenv('KEYVAULT_URL'), queue)
    assert key == 'aa'
    assert url == 'bb/cc/dd'

    with pytest.raises(Exception):
        get_key_url('invalid', os.getenv('KEYVAULT_URL'), queue)