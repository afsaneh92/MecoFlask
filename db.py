import sqlite3
import time
from random import randint

import psutil


def database():
    sqlite_file = 'db.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    conn.execute("DROP TABLE measures")
    conn.execute("CREATE TABLE measures (timestamp DATETIME, measure INTEGER, id INTEGER)")
    conn.commit()
    conn.close()


def clear_table():
    sqlite_file = 'db.sqlite'
    conn = sqlite3.connect(sqlite_file)
    sql = 'DELETE FROM measures'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    sqlite_file = 'db.sqlite'
    # timestamp_begin = 1576332717  # 01/01/14 00:00
    # timestamp_end = timestamp_begin +  60*100
    timestamp_end = time.time()
    timestamp_begin = timestamp_end-100
    pitch = 1

    try:
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        timestamp = timestamp_begin
        # id = id
        while timestamp <= timestamp_end:
            print("Iterations left :", (timestamp_end - timestamp) / pitch)
            # measure = randint(0, 9)
            measure = psutil.cpu_percent()
            conn.execute(
                "INSERT INTO measures (timestamp, measure) VALUES ({timestamp}, {measure})".format(timestamp=timestamp,
                                                                                                   measure=measure))
            conn.commit()
            timestamp += pitch
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == '__main__':
    database()
