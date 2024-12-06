import requests
from downerhelper.secrets import get_key_url
from downerhelper.gis import query_attachments, get_attachment
import base64
import re

def get_list_chunk(site_address, list_name, curr_id, key_url, queue) -> dict:
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "curr_id": curr_id
            }
        )
        if not response.ok: raise Exception('Failed to get data from SharePoint list')
        return response.json()['value']
    except Exception as e:
        queue.add('ERROR', f"Error getting SharePoint list {list_name} at {site_address}: {e}")
        raise e

def get_list(site_address, list_name, keyvault_url, queue, pagination_limit=100):
    try:
        key_url = get_key_url('get-sharepoint-list', keyvault_url, queue)
    except Exception as e:
        queue.add('ERROR', f"Error getting key/URL for SharePoint list {list_name} at {site_address}: {e}")
        raise e
    
    sp_list = []
    curr_id = 0
    count = 0
    while count < pagination_limit:
        curr_list = get_list_chunk(site_address, list_name, curr_id, key_url, queue)
        if len(curr_list) == 0: break
        sp_list.extend(curr_list)
        curr_id = curr_list[-1]['ID']
        count += 1
        
    if count == pagination_limit:
        queue.add('ERROR', f"Pagination limit reached for SharePoint list {list_name} at {site_address}")
        raise Exception('Pagination limit reached')
    
    queue.add('INFO', f"Retrieved {len(sp_list)} items from SharePoint list {list_name} at {site_address}")
    return sp_list

default_delims = [', ']
def form_list_item(attributes, title, pairs, queue, delims=None):
    if delims is None: delims = default_delims
    try:
        item = {}
        for key, value in pairs.items():
            if value is None:
                item[key] = ''
            elif isinstance(value, list):
                item[key] = combine_list_elements(attributes, value, delims, 0)
            else:
                item[key] = attributes.get(value, '')
                if item[key] is None: item[key] = ''

            if not isinstance(item[key], str): continue
            item[key] = re.sub(r"[\n\t\r]", "", item[key].strip())

        item['Title'] = title
        return item
    
    except Exception as e:
        queue.add('ERROR', f"Error forming SharePoint list item: {e}")
        raise e
    
def combine_list_elements(attributes, elems, delims, idx) -> str:
    if idx >= len(delims):
        raise Exception('Delimiter list is too short')
    
    additions = []
    for elem in elems:
        if elem is None: continue
        elif isinstance(elem, list):
            additions.append(combine_list_elements(attributes, elem, delims, idx+1))
        else:
            try:
                value = attributes.get(elem)
                if value is None: continue
                additions.append(str(value).strip())
            except Exception as e: continue

    additions = [add for add in additions if add not in [None, '']]
    return delims[idx].join(additions)

def create_list_item(item, site_address, list_name, key_url, queue):
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item": item
            }
        ) 
        if not response.ok: raise Exception('Failed to create item in SharePoint list')
        return response.json()['id']
    except Exception as e:
        queue.add('ERROR', f"Error creating SharePoint list item on {list_name} at {site_address}: {e}")
        raise e
    
def create_sharepoint_list_attachment(item_id, attachment, attachment_name, site_address, list_name, key_url, queue) -> bool:   
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item_id": item_id,
                "attachment": base64.b64encode(attachment).decode('utf-8'),
                "attachment_name": attachment_name
            },
            headers={
                'Content-Type': 'application/json'
            }
        ) 
        if not response.ok: raise Exception('Failed to create item in SharePoint list')
        return True
    
    except Exception as e:
        queue.add('ERROR', f"Error creating SharePoint list attachment on item {item_id} in {list_name} at {site_address}: {e}")
        raise e
    
def upload_attachments(token, feature_service, object_id, site_address, list_name, item_id, key_url, queue):
    detect_fail = False
    attachment_data = query_attachments(token, feature_service, object_id, queue)
    for group in attachment_data['attachmentGroups']:
        for info in group['attachmentInfos']:
            try:
                attachment = get_attachment(token, feature_service, object_id, info['id'], queue)
                create_sharepoint_list_attachment(item_id, attachment, info['name'], site_address, list_name, key_url, queue)
            except Exception as e:
                queue.add('ERROR', f"Error uploading attachment {info['name']} for object_id {object_id}: {e}")
                detect_fail = True
                continue

    if detect_fail: raise Exception("Error uploading attachment(s)")
    
def get_list_attachments(item_id, site_address, list_name, key_url, queue) -> list:   
    try:
        response = requests.post(key_url[1],
            json={
                "key": key_url[0],
                "site_address": site_address,
                "list_name": list_name,
                "item_id": item_id
            }
        )
        if not response.ok: raise Exception('Failed to get data from SharePoint list')
        return response.json()
    except Exception as e:
        queue.add('ERROR', f"Error getting SharePoint list attachments: {e}")
        return []