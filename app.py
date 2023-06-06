import streamlit as st
from controllers.user_controller import UserController
from controllers.attendance_controller import AttendanceController
from views.user_view import UserView
from views.attendance_view import AttendanceView
from utils.database import create_table_users, create_table_attendance, create_table_logs, db_path



def main():
    st.set_page_config(
    page_title="Sistema de Ponto de Funcionários",
    page_icon="📋",
    initial_sidebar_state="expanded"
    )   

    # Controllers
    user_controller = UserController(db_path)
    attendance_controller = AttendanceController(db_path)
    # Views
    user_view = UserView(user_controller)
    attendance_view = AttendanceView(user_controller, attendance_controller)

    st.sidebar.markdown("<h1><font color='#e8516f'>Ponto de Funcionários</font></h1>", unsafe_allow_html=True)
    st.sidebar.write('')

    actions = {
                "Gestão de Funcionários": ["Cadastrar", "Consultar", "Alterar", "Ativar / Desativar"],
                "Controle de Ponto": ["Registrar Ponto", "Consultar Registros","Alterar Registros","Enviar Dados"]
                }
    action_type = st.sidebar.radio("Categoria", list(actions.keys()))
    st.sidebar.write('')
    page = st.sidebar.selectbox(f"Funcionalidade", actions[action_type])

    if action_type == 'Gestão de Funcionários':
        if page == "Cadastrar":
            user_view.insert_user()
        elif page == "Consultar":
            user_view.select_users()
        elif page == "Alterar":
            user_view.update_user()
        elif page == "Ativar / Desativar":
            user_view.updatestatus_users()
    else:
        if page == "Registrar Ponto":
            attendance_view.create_attendance()
        elif page == "Consultar Registros":
            attendance_view.get_attendances()
        elif page == "Alterar Registros":
            attendance_view.change_attendance()
        elif page == "Enviar Dados":
            attendance_view.send_mail_data()



if __name__ == '__main__':
    create_table_users()
    create_table_attendance()
    create_table_logs()
    main()
