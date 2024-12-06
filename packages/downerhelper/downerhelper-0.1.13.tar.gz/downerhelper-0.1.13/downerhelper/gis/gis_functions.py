import requests
import json
import pytz
from datetime import datetime, timezone

def get_access_token(root, username, pwd, queue):
    try:
        tokenUrl = f"{root}/portal/sharing/rest/generateToken"
        payload  = f"username={username}&password={pwd}&expiration=60&client=referer&referer={root}&f=json"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json",
            'cache-control': "no-cache"
        }
        response = requests.post(tokenUrl, data=payload, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to get token")
        
        return response.json()['token']
    except Exception as e:
        queue.add('ERROR', f"Error getting access token: {e}")
        raise e
    
def query_feature_service(token, feature_service, where, queue, add_where=None):
    try:
        if add_where is not None:
            where = f"{where} and {add_where}"
        
        url = f"{feature_service}/query"
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/3.10'
        }

        result_data = {}
        features = []

        limit = 1000
        offset = 0
        count = 0
        while count < 100:
            params  = {
                'token': token, 
                'f':'json',
                'outFields': '*',
                'where': where,
                "resultRecordCount": limit,
                "resultOffset": offset
            }
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception("Failed to query feature service")
            
            json_data = json.loads(response.text)
            if 'status' in json_data.keys() and json_data['status'].lower() == 'error':
                if 'message' in json_data.keys():
                    raise Exception(json_data['message'])
                elif 'messages' in json_data.keys():
                    raise Exception(' '.join(json_data['messages']))
                else:
                    raise Exception(f'query returned an error: {json.dumps(json_data)}')
            elif 'features' not in json_data.keys():
                raise Exception(f'JSON data is unexpected shape: {json.dumps(json_data)}') 

            features.extend(json_data['features'])
            if len(json_data['features']) < limit: break
            if count == 0: result_data = json_data

            offset += limit
            count += 1

        result_data['features'] = features

        queue.add('INFO', f"Found {len(result_data['features'])} in the feature service")
        return result_data
    
    except Exception as e:
        queue.add('ERROR', f"Error querying feature service {feature_service}: {e}")
        raise e
    
def query_attachments(token, feature_service, object_id, queue):
    try:
        url = f"{feature_service}/queryAttachments"
        params  = {
            'token': token, 
            'f':'json',
            'objectIds': object_id,
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/3.10'
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to query feature service")
        elif 'error' in response.json().keys():
            raise Exception(response.json()['error']['message'])
        
        return json.loads(response.text)
    except Exception as e:
        queue.add('ERROR', f"Error querying attachments at {feature_service} for object {object_id}: {e}")
        raise e
    
def get_attachment(token, feature_service, object_id, attachment_id, queue):
    try:
        url = f"{feature_service}/{object_id}/attachments/{attachment_id}"
        params  = {
            'token': token, 
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/3.10'
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200 or response.content in [None, '']:
            raise Exception("Failed to get attachment")
        
        return response.content
    except Exception as e:
        queue.add('ERROR', f"Error getting attachment at {feature_service} for object {object_id} and {attachment_id}: {e}")
        raise e
    
def update_feature_service(token, feature_service, features, queue):
    try:
        url = f"{feature_service}/updateFeatures"
        params  = {
            'token': token, 
            'f':'json',
            'features': json.dumps(features),
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/3.10'
        }
        response = requests.post(url, headers=headers, params=params)

        if not response.ok or 'error' in response.json().keys(): 
            raise Exception("Failed to update feature service")
        
        for result in response.json()['updateResults']:
            if result['success']: continue
            raise Exception(result['error']['description'])
        
        return True
    except Exception as e:
        queue.add('ERROR', f"Error updating feature service at {feature_service}: {e}")
        raise e
    
def timestamp_to_datetime(timestamp, queue):
    try:
        if isinstance(timestamp, str): timestamp = int(timestamp)
        nz_tz = pytz.timezone('Pacific/Auckland')
        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).astimezone(nz_tz).isoformat()
    except Exception as e:
        queue.add("ERROR", f"Error converting timestamp {timestamp} to datetime: {e}")
        raise e