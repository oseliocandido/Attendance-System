import sqlite3
from models.attendance import Attendance, AttendanceName
from utils.logs import log_function_calls



class AttendanceController:
    def __init__(self, db_path):
        self.db_path = db_path

    def check_attendance(self, user_id, date, type , time):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO attendance (user_id, date, type, time) VALUES (?, ?, ?, ?)", (user_id, date, type, time))
            #conn.commit()
            conn.close()
            return Attendance(user_id, date, type, time)
        except sqlite3.IntegrityError:
            conn.rollback()
            conn.close()
            return None



    @log_function_calls
    def create_attendance(self, user_id, date, type, time):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO attendance (user_id, date, type, time) VALUES (?, ?, ?, ?)", (user_id, date, type, time))
            conn.commit()
            conn.close()
            return Attendance(user_id, date, type, time)
        except sqlite3.IntegrityError:
            conn.rollback()
            conn.close()
            return None


    @log_function_calls
    def get_attendance_by_userid(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT user_id, date, type, time FROM attendance WHERE user_id=?", (user_id,))
        attendances = []
        for row in c.fetchall():
            user_id, date, type, time = row
            attendance = Attendance(user_id, date, type, time)
            attendances.append(attendance)
        conn.close()
        return attendances


    @log_function_calls
    def modify_attendance(self, user_id, date, time, point_type):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = """
        UPDATE attendance
        SET time = ?
        WHERE user_id = ? AND date = ? AND type = ?;
        """
        try:
            c.execute(query, (time, user_id, date, point_type))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
        finally:
            conn.close()


    @log_function_calls
    def get_attendance_by_user_periods(self, user_id, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT user_id, date, type, time FROM attendance WHERE user_id=? AND date BETWEEN ? AND ?", (user_id, start_date, end_date))
        attendances = []
        for row in c.fetchall():
            user_id, date, type, time = row
            attendance = Attendance(user_id, date, type, time)
            attendances.append(attendance)
        conn.close()
        return attendances


    @log_function_calls
    def get_all_attendances_by_periods(self, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""SELECT complete_name, date, type, time FROM attendance 
                INNER JOIN users ON attendance.user_id = users.numero_identificacao
                WHERE date BETWEEN ? AND ?""", (start_date, end_date))
        attendances = []
        for row in c.fetchall():
            name, date, type, time = row
            attendance = AttendanceName(name, date, type, time)
            attendances.append(attendance)
        conn.close()
        return attendances
    
    @log_function_calls
    def delete_attendance(self, user_id, date, point_type):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""DELETE FROM attendance 
                    WHERE user_id = ? AND date = ? AND type = ?""", 
                (user_id, date, point_type))
        conn.commit()
        conn.close()

















       