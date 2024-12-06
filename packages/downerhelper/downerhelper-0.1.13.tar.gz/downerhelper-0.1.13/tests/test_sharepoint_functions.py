import pytest
from downerhelper.sharepoint import *
from downerhelper.gis import *
from downerhelper.secrets import get_key_url
import os
from uuid import uuid4
import random
from datetime import datetime, timezone, timedelta
import base64

list_name_1="Static Test List"
list_name_2="Test List"

@pytest.fixture()
def site_address():
    return os.getenv("SITE_ADDRESS")

@pytest.fixture()
def timestamp_data():
    timestamp = os.getenv("TIMESTAMP")
    timestamp_date = os.getenv("TIMESTAMP_TO_DATETIME")
    return timestamp, timestamp_date

def test_get_list(site_address, queue, keyvault_url):
    sp_list = get_list(site_address, list_name_1, keyvault_url, queue)
    expected = [
        {
            "Title": "test0",
            "Date": "2024-09-13",
            "ProjectNumber": 5,
        },
        {
            "Title": "test1",
            "Date": "2024-09-14",
            "ProjectNumber": 7.5,
        },
        {
            "Title": "test2",
            "Date": "2024-09-15",
            "ProjectNumber": 5000,
        },
    ]

    assert len(sp_list) == len(expected)

    for item in sp_list:
        for expect in expected:
            title = item['Title'] == expect['Title']
            date = item['Date'] == expect['Date']
            project_num = item['ProjectNumber'] == expect['ProjectNumber']   
            if title and date and project_num:
                break
        else:
            assert False

    with pytest.raises(Exception):
        get_list(site_address + "1", list_name_1, keyvault_url, queue)

    with pytest.raises(Exception):
        get_list(site_address, list_name_1 + "1", keyvault_url, queue)

    with pytest.raises(Exception):
        get_list(site_address, list_name_1 + "1", keyvault_url, queue, 1)

def test_form_sharepoint_item(timestamp_data, queue):
    timestamp, timestamp_date = timestamp_data

    title = 'Title'
    attributes = {
        "date": "2024-09-13",
        "project_number": 5,
        "date_&_time": timestamp_to_datetime(timestamp, queue),
    }
    pairs = {
        "Date": "date",
        "ProjectNumber": "project_number",
        "DateTime": "date_&_time",
    }
    item = form_list_item(attributes, title, pairs, queue)
    assert item['Title'] == title
    assert item['Date'] == attributes['date']
    assert item['ProjectNumber'] == attributes['project_number']
    assert item['DateTime'] == timestamp_date

    pairs["ProjectNumber"] = "project_number1"
    item = form_list_item(attributes, None, pairs, queue)
    assert item['Title'] == None
    assert item['Date'] == attributes['date']
    assert item['ProjectNumber'] == ''
    assert item['DateTime'] == timestamp_date

    with pytest.raises(Exception):
        form_list_item(attributes, title, None, queue)

    attributes = {
        "date": "2024-09-13",
        "project_number": None,
        "date_&_time": timestamp_to_datetime(timestamp, queue),
    }
    item = form_list_item(attributes, title, pairs, queue)
    assert item['Title'] == title
    assert item['Date'] == attributes['date']
    assert item['ProjectNumber'] == ''
    assert item['DateTime'] == timestamp_date

    pairs = {
        "Date": "date",
        "ProjectNumber": "project_number",
        "DateTime": None,
    }
    item = form_list_item(attributes, title, pairs, queue)
    assert item['Title'] == title
    assert item['Date'] == attributes['date']
    assert item['ProjectNumber'] == ''
    assert item['DateTime'] == ''

def random_date():
    start_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2030-12-31', '%Y-%m-%d').date()
    delta = end_date - start_date
    random_date = start_date + timedelta(days=random.randint(0, delta.days))
    return random_date.strftime('%Y-%m-%d')

def test_create_list_item(queue, site_address, keyvault_url):
    sp_list_old = get_list(site_address, list_name_2, keyvault_url, queue)
    
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)

    key_url = get_key_url('create-sharepoint-list-item', keyvault_url, queue)

    title = str(uuid4())
    attributes = {
        "date": random_date(),
        "project_number": random.randint(0, 10000),
        "date_&_time": timestamp_to_datetime(timestamp, queue),
    }
    pairs = {
        "Date": "date",
        "ProjectNumber": "project_number",
        "DateTime": "date_&_time",
    }
    item = form_list_item(attributes, title, pairs, queue)
    item_id = create_list_item(item, site_address, list_name_2, key_url, queue)
    assert int(item_id) == len(sp_list_old) + 1

    sp_list_new = get_list(site_address, list_name_2, keyvault_url, queue)
    assert len(sp_list_new) == len(sp_list_old) + 1

    for item in sp_list_new:
        if item['Title'] != title: continue
        assert item['Date'] == attributes['date']
        assert item['ProjectNumber'] == attributes['project_number']
        break
    else:
        assert False

    with pytest.raises(Exception):
        create_list_item(item, site_address + "null", list_name_2, key_url, queue)

    item['nonenone'] = 'bad'
    with pytest.raises(Exception):
        create_list_item(item, site_address, list_name_2, key_url, queue)

def test_upload_attachments(queue, site_address, gis_creds, feature_service, keyvault_url):
    root, username, pwd = gis_creds    
    
    item_key_url = get_key_url('create-sharepoint-list-item', keyvault_url, queue)

    item = {
        "Title": str(uuid4()),
        "Date": random_date(),
        "ProjectNumber": random.randint(0, 10000),
    }
    item_id = create_list_item(item, site_address, list_name_2, item_key_url, queue)
    assert item_id != None

    token = get_access_token(root, username, pwd, queue)

    object_id = '2'
    attachment_data = query_attachments(token, feature_service, object_id, queue)
    assert attachment_data != None

    expected = []
    for group in attachment_data['attachmentGroups']:
        for info in group['attachmentInfos']:
            attachment = get_attachment(token, feature_service, object_id, info['attachmentid'], queue)
            expected.append({
                'name': info['name'],
                'content': base64.b64encode(attachment).decode('utf-8')
            })

    upload_key_url = get_key_url('create-sharepoint-list-item-attachment', keyvault_url, queue)
    upload_attachments(token, feature_service, object_id, site_address, list_name_2, item_id, upload_key_url, queue)

    retrieve_key_url = get_key_url('get-sharepoint-list-item-attachment', keyvault_url, queue)
    sp_attachments = get_list_attachments(item_id, site_address, list_name_2, retrieve_key_url, queue)
    assert len(sp_attachments) == len(expected)
    for expect in expected:
        for attachment in sp_attachments:
            if attachment['name'] != expect['name']: continue
            assert attachment['content'] == expect['content']
            break
        else:
            assert False

def test_form_list_item(queue):
    delims = [' | ', ', ', ' ']
    attributes = {
        'a': '1',
        'b': '2',
        'c': '3',
        'd': '4',
        'e': 5.1,
        'f': ' 6 ',
        'g': '7',
        'h': None
    }
    pairs = {
        'a': 'b',
        'c': ['d', 'a'],
        'e': [
            [['c']],
            [['f', 'g'], 'e', [None], 'x', ['d']],
            [[]],
            'a'
        ],
        'g': None,
        't': ['e', 'h'],
        'z': ['e', 'h', 'a'],
        'y': ['h', 'a'],
        'x': 'h'
    }
    title = None
    item = form_list_item(attributes, title, pairs, queue, delims)
    print(json.dumps(item, indent=2))
    assert item == {
        'a': '2',
        'c': '4 | 1',
        'e': '3 | 6 7, 5.1, 4 | 1',
        'g': '',
        't': '5.1',
        'z': '5.1 | 1',
        'y': '1',
        'x': '',
        'Title': None
    }

    with pytest.raises(Exception):
        form_list_item(attributes, title, None, queue)