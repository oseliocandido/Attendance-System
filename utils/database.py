import sqlite3
db_path = "../data/data.db"


def create_table_users():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (numero_identificacao INTEGER PRIMARY KEY,
                complete_name TEXT,
                date_nascimento DATE,
                date_admissao DATE,
                role TEXT,
                telephone_number TEXT,
                observation TEXT,
                status TEXT DEFAULT 'Ativo')''')
    conn.commit()
    conn.close()


def create_table_attendance():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                type TEXT,
                time TEXT,
                FOREIGN KEY (user_id) REFERENCES users (numero_identificacao),
                UNIQUE (user_id, type, date))''')
    conn.commit()
    conn.close()


def create_table_logs():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS function_calls_log
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    function_type TEXT,
                    function_name TEXT, 
                    log_date TEXT, 
                    log_time TEXT,
                    args TEXT)''')
    conn.commit()
    conn.close()