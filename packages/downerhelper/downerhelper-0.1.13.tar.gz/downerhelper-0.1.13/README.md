# Downer Azure Helper

Collection of functions to wrap the Azure SDK and ArcGIS.

Assume argument are of type `str` unless stated otherwise.

## Logging

### Postgres Log Queue

Simple handler to enter logs directly to postgres databases; uses psycopg2 for connection. Creates a new `table` if does not already exist, and groups logs by `job_id`. Logs are stored in a queue and dumped on `save` method invocation. Set `print_logs=True` to print immediately to console as well.

#### Quick Setup

```python
from downerhelper.logs import setup_queue

queue = setup_queue(logger_name, job_id, table, db_config_name, keyvault_url, print_logs=False)
queue.add('INFO', "Test message!")
queue.save()
```

Store database config in Azure Key Vault with format `<dbname>,<user>,<password>,<host>`.

#### Manual Setup 

```python
from downerhelper.logs import PostgresLogQueue

db_config = {
    'dbname': <dbname>,
    'user': <user>,
    'password': <password>,
    'host': <host>,
}

queue = PostgresLogQueue(logger_name, job_id, table, db_config: dict(str, str), print_logs=False)
```

Provide database config dictionary.

### Log Check

```python
from downerhelper.logs import setup_queue

queue = setup_queue(logger_name, job_id, table, db_config_name, keyvault_url, print_logs=False)
queue.check_logs(key_url: tuple(str, str), recipients, interval_hours=24: int)
```

Check logs from the past `interval_hours`, sends an email to `recipients` for any log levels that are not `INFO`. Recipients is a string of emails with `;` delimeter. `key_url` is for the logic app to send the email.

## Key Vault Secrets

### Get Secret Value

```python
from downerhelper.secrets import get_secret_value

value = get_secret_value(secret_name, keyvault_url, queue=None: PostgresLogQueue, credential=DefaultAzureCredential()) -> str | None
```

Retrieve the value of a keyvault secret. Returns `None` on error.

### Get Config Dictionary

```python
from downerhelper.secrets import get_config_dict

config = get_config_dict(secret_name, keyvault_url, dbname=None) -> dict
```

Retrieve a database config secret stored like `<dbname>,<user>,<password>,<host>`. Raises an error if config cannot be read.

### Get Key Url Combination

```python
from downerhelper.secrets import get_key_url

key, url = get_key_url(secret_name, keyvault_url, queue=None: PostgresLogQueue) -> tuple(str, str)
```

Retrieve the key/url combination for a logic app. Store secret as `<key>/<url>` to require only one request to get the access info for a logic app (instead of two). Raises an error if secret has incorrect format.

### Form Connection String

```python
from downerhelper.secrets import form_connection_string

string = form_connection_string(storage_account, storage_account_key) -> str
```

Returns the connection string for the target storage account.

## GIS

### ArcGIS Functions

#### Get Access Token

```python
from downerhelper.gis import get_access_token

token = get_access_token(root, username, pwd, queue: PostgresLogQueue) -> str
```

Token has a 60 minute expiry. Raises an error on failure. 

#### Query Feature Service/Layer

```python
from downerhelper.gis import query_feature_service

data = query_feature_service(token, feature_service, where, queue: PostgresLogQueue, add_where=None) -> dict
```

`add_where` is an additional `where` clause, to be used if some calls have similar `where` structures. Returns arcgis return structure. Raises an error on failure.

#### Query Attachments

```python
from downerhelper.gis import query_attachments

data = query_attachments(token, feature_service, object_id, queue: PostgresLogQueue) -> dict
```

Find attachments for `object_id`. Returns arcgis return structure. Raises an error on failure.

#### Get Attachment

```python
from downerhelper.gis import get_attachment

attachment = get_attachment(token, feature_service, object_id, attachment_id, queue: PostgresLogQueue)
```

Get attachment data for `attachment_id` on `object_id`. Returns attachment content directly. Raises an error on failure.

#### Update Feature Service

```python
from downerhelper.gis import update_feature_service

update_feature_service(token, feature_service, features: list, queue: PostgresLogQueue)
```

Argument `features` is defined by arcgis docs. Raises an error on failure.

#### Timestamp To Datetime

```python
from downerhelper.gis import timestamp_to_datetime

date_str = timestamp_to_datetime(timestamp: int | str, queue: PostgresLogQueue)
```

Convert arcgis timestamp to datetime string. Raises an error on failure.

## Sharepoint

Note: sharepoint list display names (column names) are often not the same as the data label. To find data label you can,
    
1. sort by the target column, in the url find the `sortField` param.
2. go to column settings and select the target column, then in the url find the `Field` param.

### Get List

```python
from downerhelper.sharepoint import get_list

sp_list = get_list(site_address, list_name, keyvault_url, queue: PostgresLogQueue, pagination_limit=100: int) -> list(dict)
```

Returns sharepoint list items as a list of dictionary data. Keys are sharepoint data labels not display names. Raises an error on failure.

### Form List Item

```python
from downerhelper.sharepoint import form_list_item

form_list_item(attributes: dict(str, str), title, pairs: dict(str, str), queue: PostgresLogQueue, delims=[', ']: list(str)) -> dict
```

Uses arcgis record `attributes` from `query_feature_service` functions. Argument `pairs` represents the mapping of sharepoint data labels (keys of return dict) to arcgis attribute keys (values of return dict). Raises an error on failure.

### Create List Item

```python
from downerhelper.sharepoint import create_list_item

item = create_list_item(item: dict(str, str), site_address, list_name, key_url: tuple(str, str), queue: PostgresLogQueue)
```

Uploads an item to target sharepoint list, where `key_url` represents the key/url access combination of the logic app. Raises an error on failure.

### Upload Attachments

```python
from downerhelper.sharepoint import upload_attachments

upload_attachments(token, feature_service, object_id, site_address, list_name, item_id, key_url: tuple(str, str), queue: PostgresLogQueue)
```

Uploads all attachments for arcgis target `object_id` to sharepoint. Raises an error on failure (one or more attachments failing to upload triggers failure).

### Get List Item Attachments

```python
from downerhelper.sharepoint import get_list_attachments

attachmnets = get_list_attachments(item_id, site_address, list_name, key_url: tuple(str, str), queue: PostgresLogQueue) -> list
```

Returns empty list on failure.

## Logic App

### Send Email (Outlook)

```python
from downerhelper.logicapp import send_email

send_email(key_url: tuple(str, str), recipients: str | list(str), subject, body, attachments=[], cc=[]: str | list(str), bcc=[]: str | list(str), importance="Normal": ["Normal", "Low", "High"]) -> bool
```

`key_url` is for the logic app access. All `recipients`, `cc` and `bcc` are emails, supplied as a string delimited by `;` or a list of strings. `attachments` is a list of dictionaries like 
```python
{
    "Name": filename: str,
    "ContentBytes": content: str | bytes
}
```
where `ContentBytes` is either a base64 encoded string or bytes that will be encoded.

Raises an exception on failure.

## Warning!

The following snippet shows incorrect usage. Modules must be declared and imported seperately.

```python
import downerhelper

value = downerhelper.secrets.get_secret_value(secret_name, keyvault_url)
```