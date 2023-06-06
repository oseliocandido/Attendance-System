import datetime
import sqlite3
from models.user import User, UserDTO
from utils.logs import log_function_calls



class UserController:
    def __init__(self, db_path):
        self.db_path = db_path


    @log_function_calls
    def insert_employee(self, inputs):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            insert_query = """INSERT INTO users (numero_identificacao, complete_name, 
                            date_nascimento, date_admissao, role, telephone_number, observation) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)"""
            c.execute(insert_query, tuple(inputs[key] for key in inputs.keys()))
            conn.commit()
            conn.close()
            return User(**inputs)
        except sqlite3.IntegrityError:
            conn.close()
            return None


    @log_function_calls
    def select_info_employees(self, selected_columns):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        columns_str = ", ".join(selected_columns)
        query = f"SELECT {columns_str} FROM users"
        c.execute(query)
        users = []
        for row in c.fetchall():
            user_data = dict(zip(selected_columns, row))
            user = UserDTO(**user_data)
            users.append(user)
        conn.close()
        return users


    @log_function_calls
    def update_employees_status(self, id, status):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        fetch_query = "SELECT * FROM users WHERE numero_identificacao=?"
        c.execute(fetch_query, (id,))
        row = c.fetchone()
        columns = [description[0] for description in c.description]
        user_data = dict(zip(columns, row))
        # user_data = {}
        # user_data['numero_identificacao'] = row[0]

        if user_data is None:
            return None
        user = UserDTO(**user_data)

        status_str = "Ativo" if status else "Inativo"

        update_query = "UPDATE users SET status=? WHERE numero_identificacao=?"
        c.execute(update_query, (status_str, id))
        conn.commit()
        return user


    @log_function_calls
    def update_employee(self, selected_columns, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Prepare the other columns and values for the update query
        columns_values_for_update = [(column, value) for column, value in selected_columns if column != 'numero_identificacao']
        set_clause = ", ".join(f"{column} = ?" for column, _ in columns_values_for_update)
        update_query = f"UPDATE users SET {set_clause} WHERE numero_identificacao = ?"

        # Extract the new values (excluding numero_identificacao) and append the user_id
        values = [new_value.isoformat() if isinstance(new_value, datetime.date) else new_value for _, new_value in columns_values_for_update]
        values.append(user_id)

        c.execute(update_query, values)
        conn.commit()

        fetch_query = "SELECT * FROM users WHERE numero_identificacao=?"
        c.execute(fetch_query, (user_id,))
        row = c.fetchone()

        if row is None:
            return None

        user_data = dict(zip([column[0] for column in c.description], row))
        user = UserDTO(**user_data)
        return user
    