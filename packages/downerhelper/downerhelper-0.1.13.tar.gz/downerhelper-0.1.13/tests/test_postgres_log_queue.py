import pytest
from downerhelper.logs import PostgresLogQueue, setup_queue
from downerhelper.secrets import get_secret_value, get_config_dict, get_key_url
import os
from uuid import uuid4
import psycopg2 as pg

def test_class_valid_queue(keyvault_url):
    logger_name = 'pytest'
    job_id = str(uuid4())
    table = os.getenv('LOG_TABLE')
    
    queue = setup_queue(logger_name, job_id, table, 'db-config-1', keyvault_url)

    messages = [str(uuid4()) for _ in range(4)]
    for message in messages:
        queue.add('INFO', message)

    queue.save()

    try:
        db_config = get_config_dict('db-config-1', keyvault_url)
        conn = pg.connect(**db_config)
        cur = conn.cursor()
        cur.execute(f"""select name, job_id 
        from {table}
        where job_id = '{job_id}';""")
        rows = cur.fetchall()
    except:
        assert False

    assert len(rows) >= len(messages)
    for row in rows:
        assert row[0] == logger_name
        assert row[1] == job_id

def test_invalid_setup_queue(keyvault_url):
    with pytest.raises(Exception):
        setup_queue(None, 'a', 'a', 'db-config-1', keyvault_url)

    with pytest.raises(Exception):
        setup_queue('a', None, 'a', 'db-config-1', keyvault_url)

    with pytest.raises(Exception):
        setup_queue('a', 'a', None, 'db-config-1', keyvault_url)

    with pytest.raises(Exception):
        setup_queue('a', 'a', 'a', 'none-exist', keyvault_url)

    with pytest.raises(Exception):
        setup_queue('a', 'a', 'a', 'db-config-1', keyvault_url + 'invalid')

def test_invalid_queue(keyvault_url):
    db_config_str = get_secret_value('db-config-1', keyvault_url)
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    db_config = {k: v for k, v in zip(keys, db_config_split)}

    with pytest.raises(Exception):
        PostgresLogQueue(None, 'a', 'a', db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', None, 'a', db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', 'a', None, db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', 'a', 'a', {})

def test_check_logs(keyvault_url):
    logger_name = 'pytest-check-logs'
    job_id = str(uuid4())
    table = os.getenv('LOG_TABLE')

    queue = setup_queue(logger_name, job_id, table, 'db-config-1', keyvault_url)

    messages = [str(uuid4()) for _ in range(4)]
    for message in messages:
        queue.add('INFO', message)

    error_num = 2
    messages = [str(uuid4()) for _ in range(error_num)]
    for message in messages:
        queue.add('ERROR', message)

    warn_num = 1
    messages = [str(uuid4()) for _ in range(warn_num)]
    for message in messages:
        queue.add('WARN', message)

    queue.save()

    try:
        db_config = get_config_dict('db-config-1', keyvault_url)
        conn = pg.connect(**db_config)
        cur = conn.cursor()
        cur.execute(f"""select count(*)
from {table}
where job_id = '{job_id}'
and is_checked = false
and levelname != 'INFO';""")
        row = cur.fetchone()

        assert row[0] == error_num + warn_num

        key_url = get_key_url(os.getenv('SEND_EMAIL_SECRET'), keyvault_url, queue)
        queue.check_logs(key_url, 'marcus.oates@downergroup.com', 1)

        cur.execute(f"""select count(*)
from {table}
where job_id = '{job_id}'
and is_checked = false
and levelname != 'INFO';""")
        row = cur.fetchone()

        assert row[0] == 0

        cur.execute(f"""select count(*)
from {table}
where job_id = '{job_id}'
and is_checked = true
and levelname != 'INFO';""")
        row = cur.fetchone()

        assert row[0] == error_num + warn_num

    except:
        assert False