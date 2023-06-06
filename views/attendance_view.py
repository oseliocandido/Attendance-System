import streamlit as st
import pandas as pd
from models.attendance import Attendance
from datetime import datetime, timedelta
from utils.authentication import is_authenticated_password
from utils.formatting import brazilian_date, pretty_html_table
from utils.sendmail import send_email
from utils.correctperiods import current_plus_two_previous_months
from streamlit_extras.let_it_rain import rain
from dateutil.relativedelta import relativedelta
from pytz import timezone



class AttendanceView:
    options = ["Entrada", "Entrada Almoço", "Saída Almoço", "Saída"]
    def __init__(self, user_controller, attendance_controller):
        self.user_controller = user_controller
        self.attendance_controller = attendance_controller

    def create_attendance(self):
        st.markdown('<h4 style="color:white;">Registrar Ponto</h4>', unsafe_allow_html=True)
        users = self.user_controller.select_info_employees(['numero_identificacao','complete_name','status'])
        user_names = [user.complete_name for user in users if user.status == "Ativo"]
        selected_user = st.selectbox("Funcionários Ativos", user_names)

        current_datetime = datetime.now(timezone('America/Sao_Paulo'))
        current_date_dmy = current_datetime.strftime("%d-%m-%Y")
        current_date_ymd = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M")

        #Brazilian day of week
        day_of_week = current_datetime.strftime("%A")
        day_names_mapping = {
                            "Monday": "segunda-feira",
                            "Tuesday": "terça-feira",
                            "Wednesday": "quarta-feira",
                            "Thursday": "quinta-feira",
                            "Friday": "sexta-feira",
                            "Saturday": "sábado",
                            "Sunday": "domingo"
                        }
        brazilian_day_week = day_names_mapping.get(day_of_week)

        st.markdown(f'<h3 style="color:white;"> 📅 <span style="color:#d05573;">{current_date_dmy} [{brazilian_day_week}]</span></h3>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:white;"> ⏰ <span style="color:green;">{current_time}</span> </h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        point_type = col1.radio(
            "Tipo de Ponto", AttendanceView.options)

        if selected_user is not None:
            if st.button("Registrar"):
                user_id = users[user_names.index(selected_user)].numero_identificacao
                attendance = self.attendance_controller.check_attendance(user_id, current_date_ymd, point_type, current_time)
                if isinstance(attendance, Attendance):
                    self.attendance_controller.create_attendance(user_id, current_date_ymd, point_type, current_time , log_call=True)
                    st.success(f"Ponto registrado com sucesso, {str(selected_user).split()[0]}!")
                    #Ballons if its friday and the employee is leaving
                    if current_datetime.weekday() in [4,5] and point_type == 'Saída':
                        rain(
                                emoji="🍻",
                                font_size=40,
                                falling_speed=3,
                                animation_length="infinite",
                            )
                    else:
                        pass
                else:
                    st.error("Este ponto já foi registrado")
                    st.error("Escolha outros valores")
        else:
            st.error('Sem Funcionário Cadastrado')


    def change_attendance(self):
        st.markdown('<h4 style="color:white;">Alteração de Ponto', unsafe_allow_html=True)
        users = self.user_controller.select_info_employees(['numero_identificacao','complete_name','status'])
        user_names = [user.complete_name for user in users if user.status == "Ativo"]
        selected_user = st.selectbox("Funcionário", user_names)
        point_type = st.selectbox("Tipo de Ponto", ["Entrada", "Entrada Almoço", "Saída Almoço", "Saída"])
        date = st.date_input(label="Data", help="Formato Ano/Mês/Dia",max_value=datetime.now()).strftime('%Y-%m-%d')

        if selected_user is not None:
            user_id = users[user_names.index(selected_user)].numero_identificacao
            attendances = self.attendance_controller.get_attendance_by_userid(user_id)
            attendance_data = {
                "Data": [attendance.date for attendance in attendances],
                "time": [attendance.time for attendance in attendances],
                "type": [attendance.type for attendance in attendances]
            }

            combined_attendance_data = list(zip(attendance_data["Data"], attendance_data["type"], attendance_data["time"]))
            matching_attendance = [(item[0], item[1], item[2]) for item in combined_attendance_data if item[1] == point_type and item[0] == date]
            portuguese_date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%d-%m-%Y')

            if matching_attendance:
                previous_date, previous_type, previous_time = matching_attendance[0]
                st.info(f'Ponto de {point_type} de {selected_user} em {portuguese_date} foi às {previous_time}.')
                new_time = st.time_input("Novo Horário",step=300).strftime("%H:%M")
                st.warning(f'Ponto de {point_type} de {selected_user} em {portuguese_date} será às {new_time}.')
                app_pass = st.text_input(label=":red[Senha]", type="password")
                is_correct_password = is_authenticated_password(app_pass)
                if app_pass == '':
                    pass
                elif not is_correct_password:
                    st.error('Senha Incorreta!')
                if is_correct_password:
                    if st.button("Alterar Ponto"):
                        self.attendance_controller.modify_attendance(user_id, date, new_time, point_type,log_call=True)
                        st.success("Ponto alterado com sucesso!")
            else:
                st.info(f'{selected_user} não possui ponto do tipo {point_type} em {portuguese_date}')

                current_datetime = datetime.now(timezone('America/Sao_Paulo'))
                new_time = st.time_input("Novo Horário",step=300,value=current_datetime).strftime("%H:%M")

                app_pass = st.text_input(label=":red[Senha]", type="password")
                is_correct_password = is_authenticated_password(app_pass)
                if app_pass == '':
                    pass
                elif not is_correct_password:
                    st.error('Senha Incorreta!')
                if is_correct_password:
                    if st.button("Inserir Ponto"):
                        self.attendance_controller.create_attendance(user_id, date, point_type, new_time, log_call=True)
                        st.success("Ponto inserido com sucesso!")
        else:
            st.error(f'Sem dados para {selected_user}.')

    
    def get_attendances(self):
        st.markdown('<h4 style="color:white;">Registros de Pontos', unsafe_allow_html=True)
        users = self.user_controller.select_info_employees(['numero_identificacao','complete_name'])
        user_names = [user.complete_name for user in users]
        selected_user = st.selectbox("Funcionários", user_names)

        month_translation = {
        'January': 'Janeiro',
        'February': 'Fevereiro',
        'March': 'Março',
        'April': 'Abril',
        'May': 'Maio',
        'June': 'Junho',
        'July': 'Julho',
        'August': 'Agosto',
        'September': 'Setembro',
        'October': 'Outubro',
        'November': 'Novembro',
        'December': 'Dezembro'
    }

        months_options = current_plus_two_previous_months(month_translation)
        selected_months_pt = st.multiselect("Período", options=list(months_options.keys())[::-1])  # [::-1] is used to reverse the order

        if st.button("Consultar"):
            if selected_user is not None:
                user_id = users[user_names.index(selected_user)].numero_identificacao
                df_list = []  
                for month_pt in selected_months_pt:
                    month_english = months_options[month_pt]
                    selected_month_datetime = datetime.strptime(month_english, '%B %Y')
                    next_month_datetime = selected_month_datetime + relativedelta(months=1)

                    selected_month_start = selected_month_datetime.strftime('%Y-%m-%d')
                    selected_month_end = next_month_datetime.strftime('%Y-%m-%d')

                    attendances = self.attendance_controller.get_attendance_by_user_periods(user_id, selected_month_start, selected_month_end, log_call=True)

                    if attendances:
                        attendance_data = {
                            "Data": [attendance.date for attendance in attendances],
                            "Time": [attendance.time for attendance in attendances],
                            "Type": [attendance.type for attendance in attendances]
                        }
                        df = pd.DataFrame(attendance_data)
                        df = df.pivot(index='Data', columns='Type', values='Time').reset_index()
                        df.index.name = "Id_Registro"
                        df.index = df.index + 1
                        df_list.append(df)  # Add the df to the list

                # Concatenate all the dataframes in the list
                if df_list:
                    all_df = pd.concat(df_list)
                    all_df['Data'] = pd.to_datetime(all_df['Data'])
                    all_df = all_df.sort_values(by="Data", ascending=False)
                    all_df = all_df.reindex(columns= ['Data'] + AttendanceView.options)
                    all_df = all_df.fillna('-')
                    all_df = brazilian_date(all_df, ['Data'])
                    pretty_html_table(all_df)
                else:
                    st.error(f'Sem registros para {selected_user} no período')


    def delete_attendance(self):
        st.markdown('<h4 style="color:white;">Deletar Registros', unsafe_allow_html=True)
        users = self.user_controller.select_info_employees(['numero_identificacao','complete_name','status'])
        user_names = [user.complete_name for user in users if user.status == "Ativo"]
        selected_user = st.selectbox("Funcionário", user_names)
        point_type = st.selectbox("Tipo de Ponto", AttendanceView.options)
        date = st.date_input(label="Data", help="Formato Ano/Mês/Dia",max_value=datetime.now()).strftime('%Y-%m-%d')

        if selected_user is not None:
            user_id = users[user_names.index(selected_user)].numero_identificacao
            attendances = self.attendance_controller.get_attendance_by_userid(user_id)
            attendance_data = {
                "Data": [attendance.date for attendance in attendances],
                "time": [attendance.time for attendance in attendances],
                "type": [attendance.type for attendance in attendances]
            }

            combined_attendance_data = list(zip(attendance_data["Data"], attendance_data["type"], attendance_data["time"]))
            matching_attendance = [(item[0], item[1], item[2]) for item in combined_attendance_data if item[1] == point_type and item[0] == date]
            portuguese_date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%d-%m-%Y')

            if matching_attendance:
                previous_date, previous_type, previous_time = matching_attendance[0]
                st.info(f'Ponto de {point_type} de {selected_user} em {portuguese_date} é {previous_time}.')
                app_pass = st.text_input(label=":red[Senha]", type="password")
                is_correct_password = is_authenticated_password(app_pass)
                if app_pass == '':
                    pass
                elif not is_correct_password:
                    st.error('Senha Incorreta!')
                if is_correct_password:
                    if st.button("Deletar Ponto"):
                        self.attendance_controller.delete_attendance(user_id, date, point_type, log_call=True)
                        st.success("Ponto deletado com sucesso!")
            else:
                st.error(f'{selected_user} não possui ponto do tipo {point_type} em {portuguese_date}')
        else:
            st.error(f'Sem dados para {selected_user}.')







    def send_mail_data(self):
        st.markdown('<h4 style="color:white;">Registros de Pontos', unsafe_allow_html=True)
        month_translation = {
            'January': 'Janeiro',
            'February': 'Fevereiro',
            'March': 'Março',
            'April': 'Abril',
            'May': 'Maio',
            'June': 'Junho',
            'July': 'Julho',
            'August': 'Agosto',
            'September': 'Setembro',
            'October': 'Outubro',
            'November': 'Novembro',
            'December': 'Dezembro'
        }

        months_options = current_plus_two_previous_months(month_translation)
        selected_month_pt = st.selectbox("Período", options=list(months_options.keys())[::-1])  # [::-1] is used to reverse the order

        if st.button("Enviar"):
            month_english = months_options[selected_month_pt]
            selected_month_datetime = datetime.strptime(month_english, '%B %Y')
            next_month_datetime = selected_month_datetime + relativedelta(months=1)

            selected_month_start = selected_month_datetime.strftime('%Y-%m-%d')
            selected_month_end = next_month_datetime.strftime('%Y-%m-%d')
            attendances = self.attendance_controller.get_all_attendances_by_periods(selected_month_start, selected_month_end, log_call=True)
            if attendances:
                attendance_data = {
                    "Data": [attendance.date for attendance in attendances],
                    "Time": [attendance.time for attendance in attendances],
                    "Type": [attendance.type for attendance in attendances],
                    "Nome": [attendance.name for attendance in attendances]
                }
                df = pd.DataFrame(attendance_data)
                df.set_index(['Data', 'Nome'], inplace=True)
                df = df.pivot(columns='Type', values='Time')
                df.reset_index(inplace=True)
                df = brazilian_date(df, ['Data'])
                df.index.name = "Id_Registro"
                df.index = df.index + 1
                df.fillna('-',inplace=True)
                send_email(df,selected_month_pt)
            else:
                st.error(f'Sem registros para o período selecionado')
                return
