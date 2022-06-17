import os
import psycopg2
from psycopg2._psycopg import cursor as _cursor
from urllib.parse import urlparse


def connect_db() -> _cursor | None:
    try:
        db_url = os.environ.get("DATABASE_URL")

        result = urlparse(db_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        connection = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        global cursor
        cursor = connection.cursor()
        return cursor
    except:
        return None


def get_subjects(scheme: str, branch: str, semester: str) -> list[tuple]:
    cursor.execute("SELECT * FROM subject WHERE scheme=%(scheme)s AND branch=%(branch)s AND semester=%(semester)s;",
                   {"scheme": scheme, "branch": branch, "semester": int(semester)})
    data = cursor.fetchall()
    return data

def get_notes(subject: str, module: str) -> tuple:
    cursor.execute("SELECT * FROM file WHERE subject=%(subject)s AND module=%(module)s;",
                    {"subject": subject.upper(), "module": int(module)})
    data = cursor.fetchone()
    return data
