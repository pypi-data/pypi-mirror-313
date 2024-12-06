import logging
import psycopg2 as pg
from psycopg2 import sql
from datetime import datetime, timezone
from downerhelper.secrets import get_config_dict
import requests
from downerhelper.logicapp import send_email

class PostgresLogQueue():
    def __init__(self, logger_name, job_id, table, db_config, print_logs=False):
        try:
            if '' in [logger_name, job_id, table] or \
                None in [logger_name, job_id, table] or db_config == {}:
                raise Exception("Invalid parameters")
            self.logger_name = logger_name
            self.job_id = job_id
            self.db_config = db_config
            self.table = table
            self.print_logs = print_logs
            self.queue = [
                {
                    'levelname': 'INFO',
                    'message': f'queue: {logger_name} created for job_id: {job_id}',
                    'created_at': datetime.now(timezone.utc)
                }
            ]
        except Exception as e:
            logging.error(f"Error setting up PostgresLogHandler: {e}")
            raise e

    def add(self, levelname, message):
        self.queue.append({
            'levelname': levelname,
            'message': message,
            'created_at': datetime.now(timezone.utc)
        })
        if not self.print_logs: return
        
        if levelname == 'ERROR':
            logging.error(message)
        elif levelname == 'WARNING':
            logging.warning(message)
        elif levelname == 'DEBUG':
            logging.debug(message)
        else:
            logging.info(message)

    def save(self):
        try:
            conn = pg.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("set time zone 'UTC'")
            cursor.execute(f"""
            create table if not exists {self.table} (
                id serial primary key,
                created_at timestamptz default now(),
                name varchar(255),
                levelname varchar(50),
                message text,
                job_id varchar(255) not null,
                is_checked boolean default false
            )""")
            conn.commit()
            
            for log in self.queue:
                cursor.execute(f"""
                insert into {self.table} (name, levelname, message, job_id, created_at)
                values (%s, %s, %s, %s, %s)
                """, (self.logger_name, log['levelname'], log['message'], self.job_id, log['created_at']))
            conn.commit()

            if cursor: cursor.close()
            if conn: conn.close()

            self.queue = []

        except Exception as e:
            logging.error(f"Error saving logs: {e}")
            if cursor: cursor.close()
            if conn: conn.close()

    def check_logs(self, key_url, recipients, interval_hours=24):
        try:
            conn = cur = None
            conn = pg.connect(**self.db_config)
            cur = conn.cursor()

            cur.execute(sql.SQL("""
                select name, levelname, message, job_id, id
                from {}
                where levelname != 'INFO'
                and is_checked = false
                and created_at > now() - interval {}::interval;
            """).format(
                sql.Identifier(self.table),
                sql.Literal(f'{interval_hours} hours')
            ))
            rows = cur.fetchall()

            if len(rows) == 0:
                self.add('INFO', 'No errenous logs')
                self.save()
                return

            data = {}
            ids = []
            for row in rows:
                key = f"{row[0]}:{row[3]}"
                if key not in data.keys(): data[key] = []
                data[key].append({
                    'levelname': row[1],
                    'message': row[2]
                })
                ids.append(row[4])
            flows_in_error = set([k.split(':')[0] for k in data.keys()])

            table_html = """
            <table border="1">
                <tr>
                    <th>Name</th>
                    <th>Level</th>
                    <th>Message</th>
                    <th>Job ID</th>
                </tr>
            """
            for row in rows:
                table_html += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                </tr>
                """

            subject = f"Log Check: {self.table}"
            body = f"""Flows in error: {', '.join(flows_in_error)}<br><br>{table_html}"""
            send_email(key_url, recipients, subject, body)

            cur.execute(sql.SQL("""
                update {}
                set is_checked = true
                where id = any(%s);
            """).format(
                sql.Identifier(self.table)
            ), (ids,))
            conn.commit()

        except Exception as e:
            self.add('ERROR', f"Error checking logs: {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()
            self.save()


def setup_queue(logger_name, job_id, table, db_config_name, keyvault_url, print_logs=False):
    try:
        db_config = get_config_dict(db_config_name, keyvault_url)
        return PostgresLogQueue(logger_name, job_id, table, db_config, print_logs)
    except Exception as e:
        logging.error(f"Error setting up logger: {e}")
        raise Exception("Error setting up logger")