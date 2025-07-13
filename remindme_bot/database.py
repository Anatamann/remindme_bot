import sqlite3
from remindme_bot import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS

def init_database():
    """Initialize SQLite database and create necessary tables"""
    try:
        with sqlite3.connect('remindme_bot.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rm_check_table (
                    id INTEGER PRIMARY KEY,
                    task_date TEXT
                )
            ''')
            conn.commit()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminder_table (
                    id INTEGER PRIMARY KEY,
                    usr_id TEXT,
                    task TEXT,
                    created_at TEXT,
                    rm_time FLOAT,
                    remind_at TEXT,
                    rm_status INTEGER
                )
            ''')
            conn.commit()
    except OSError:
        print(DB_WRITE_ERROR)

def remind_in(task, time_target, usr_id, created_at, rm_at, status=0):
    try:
        with sqlite3.connect('remindme_bot.db') as conn:
            cursor = conn.cursor()
            if not status:
                cursor.execute('''
                    INSERT INTO reminder_table (usr_id, task, created_at, rm_time, remind_at,rm_status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ( str(usr_id), str(task), str(created_at), float(time_target), str(rm_at), int(status) ))
            else:
                return ("Logical Error possibly want to update the status.")
    except Exception as e:
        print(e)

def remind_check():
    try:
        rm_status = 0
        limit = 50
        with sqlite3.connect('remindme_bot.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, usr_id, remind_at, task 
            FROM reminder_table
            WHERE rm_status=?
            LIMIT ?
            ''',(int(rm_status),int(limit)))
        rm_ids = cursor.fetchall()
        if not rm_ids:
            return
        else:
            return [{'rm_id': r[0], 'user_id': r[1], 'remind_at': r[2], 'task': r[3]} for r in rm_ids]
    except Exception as e:
        print(e)

def remind_update(id,status=1):
    try:
        with sqlite3.connect('remindme_bot.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE reminder_table
            SET rm_status=?
            WHERE id=?
            ''', (int(status), str(id)))
            conn.commit()
            return
    except Exception as e:
            print(e)

def rm_check_table_up(task_date, id=1):
    try:
        with sqlite3.connect('remindme_bot.db') as conn:
            cursor = conn.cursor()
            cursor.execute ('''
                UPDATE rm_check_table
                SET task_date=?
                WHERE id=?
                ''', (str(task_date), int(id)))
            conn.commit()
    except Exception as e:
        print(e)