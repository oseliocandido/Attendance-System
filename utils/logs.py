import sqlite3
from datetime import datetime
from utils.database import db_path
from pytz import timezone

mapping_controller_functions_to_log = {
    'insert_employee': 'inserir_funcionario',
    'select_info_employees': 'selecionar_informacoes_funcionarios',
    'update_employee': 'atualizar_funcionario',
    'update_employees_status': 'update_status_funcionario',
    'create_attendance': 'criar_frequencia',
    'get_attendance_by_user_periods': 'obter_frequencia_por_periodo',
    'get_attendance_by_userid': 'obter_frequencia_por_id_usuario',
    'modify_attendance': 'alterar_frequencia',
    'get_all_attendances_by_periods': 'enviar_email',
    'delete_attendance':'deletar_frequencia'
}

def log_function_calls(func):
    def wrapper(*args,**kwargs):
        log_call = kwargs.pop('log_call', False)
        if log_call:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            function_name = mapping_controller_functions_to_log.get(str(func.__name__))
            function_type = 'Usuário' if 'funcionario' in function_name  else 'Frequência'
            log_date = datetime.now().strftime('%d-%m-%Y')
            log_time = datetime.now(timezone('America/Sao_Paulo')).strftime("%H:%M")

            c.execute("""INSERT INTO function_calls_log (function_type, function_name, 
                                log_date, log_time, args) 
                                VALUES (?, ?, ?, ?, ?)""",
                    (function_type, function_name, log_date, log_time, str(args[1])))
            conn.commit()
            conn.close()
        return func(*args)
    return wrapper
