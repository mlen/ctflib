from .context import ctflib
from functools import partial
import sqlite3


def oracle(conn, collection, position):
    try:
        sql = 'SELECT ' + ctflib.db.sqlite('sqlite_version()', position, collection).error()
        conn.execute(sql)
        return True
    except sqlite3.OperationalError:
        return False


def test_blind_injection():
    conn = sqlite3.connect(':memory:')
    version = next(conn.execute('select sqlite_version()'))[0]
    assert ctflib.blind.extract(partial(oracle, conn)) == version
