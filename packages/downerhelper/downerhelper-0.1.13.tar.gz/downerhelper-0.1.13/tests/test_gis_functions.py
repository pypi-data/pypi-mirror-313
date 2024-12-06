import pytest
from downerhelper.gis import *
from downerhelper.logs import setup_queue
import os
from uuid import uuid4

@pytest.fixture(scope="module")
def queue(keyvault_url):
    return setup_queue('pytest', str(uuid4()), os.getenv('LOG_TABLE'), 'db-config-1', keyvault_url)

@pytest.fixture(scope="module")
def token(gis_creds, queue):
    root, username, pwd = gis_creds
    return get_access_token(root, username, pwd, queue)

def test_get_token(gis_creds, queue):
    root, username, pwd = gis_creds    
    token = get_access_token(root, username, pwd, queue)
    assert token != None
    assert isinstance(token, str)
    assert len(token) > 0

    with pytest.raises(Exception):
        get_access_token('https://gis.nosite.co.au', username, pwd, queue)

    with pytest.raises(Exception):
        get_access_token(root, 'username', pwd, queue)

    with pytest.raises(Exception):
        get_access_token(root, username, 'password', queue)

def test_query_feature_service(token, queue):
    query_result = query_feature_service(token, os.getenv('FEATURE_SERVICE'), '1=1', queue)
    assert isinstance(query_result, dict)

    expected = [
        {
            "marktest": None,
            "test_string": None
        },
        {
            "marktest": 'mark1',
            "test_string": 'string1'
        },
        {
            "marktest": 'mark2',
            "test_string": 'test string 2'
        }
    ]
    found = 0
    for feature in query_result['features']:
       attributes = feature['attributes']
       for expect in expected:
            field1 = attributes['marktest'] == expect['marktest']
            field2 = attributes['test_string'] == expect['test_string']
            if not (field1 and field2): continue
            found += 1
            break
    assert found == len(expected)

    with pytest.raises(Exception):
        query_feature_service(token, os.getenv('FEATURE_SERVICE'), '1', queue)

    with pytest.raises(Exception):
        query_feature_service('', os.getenv('FEATURE_SERVICE'), '1=1', queue)

def test_query_get_attachments(token, queue):
    object_id = '3'
    attachment_data = query_attachments(token, os.getenv('FEATURE_SERVICE'), object_id, queue)
    assert attachment_data['attachmentGroups'] == []

    object_id = '2'
    attachment_data = query_attachments(token, os.getenv('FEATURE_SERVICE'), object_id, queue)
    expected = [
        {
            'att_name': 'test.txt',
            'content_type': 'text/plain',
            'name': 'test.txt',
        },
        {
            'att_name': 'B3018_discsLabels.jpg',
            'content_type': 'image/jpeg',
            'name': 'B3018_discsLabels.jpg',
        }
    ]
    found = 0
    for group in attachment_data['attachmentGroups']:
        for info in group['attachmentInfos']:
            attachment = get_attachment(token, os.getenv('FEATURE_SERVICE'), object_id, info['attachmentid'], queue)
            assert isinstance(attachment, bytes)
            for expect in expected:
                field1 = info['name'] == expect['name']
                field2 = info['att_name'] == expect['att_name']
                field3 = info['contentType'] == expect['content_type']
                if not (field1 and field2 and field3): continue
                found += 1
                break
            
    assert found == len(expected)

    with pytest.raises(Exception):
        query_attachments(token, os.getenv('FEATURE_SERVICE'), 'none_id', queue)

def test_update_feature_service(token, queue):
    features = [
        {
            'attributes': {
                'marktest': str(uuid4()),
                'test_string': str(uuid4()),
                'objectid': 4
            }
        }
    ]
    assert update_feature_service(token, os.getenv('FEATURE_SERVICE'), features, queue)

    query_result = query_feature_service(token, os.getenv('FEATURE_SERVICE'), '1=1', queue)
    for feature in query_result['features']:
        attributes = feature['attributes']
        if attributes['objectid'] != features[0]['attributes']['objectid']: continue
        assert attributes['marktest'] == features[0]['attributes']['marktest']
        assert attributes['test_string'] == features[0]['attributes']['test_string']

    features = [
        {
            'attributes': {
                'marktest': str(uuid4()),
                'test_string': str(uuid4()),
                'objectid': -1
            }
        }
    ]
    with pytest.raises(Exception):
        update_feature_service(token, os.getenv('FEATURE_SERVICE'), features, queue)

    with pytest.raises(Exception):
        update_feature_service(token, os.getenv('FEATURE_SERVICE'), None, queue)

def test_timestamp_to_datetime(queue):
    date = timestamp_to_datetime(os.getenv('TIMESTAMP'), queue)
    assert date == os.getenv('TIMESTAMP_TO_DATETIME')