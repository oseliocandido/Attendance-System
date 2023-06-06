import streamlit as st
import pandas as pd
import time
from datetime import datetime
from models.user import User
from utils.authentication import is_authenticated_password
from utils.formatting import brazilian_date, pretty_html_table
from utils.validation import is_numeric_field, validate_phone_number, is_correct_name, is_6_chars_long



class UserView:
    def __init__(self, user_controller):
        self.user_controller = user_controller


    def insert_user(self):
        st.markdown('<h4 style="color:white;">Cadastro de Funcionários</h4>', unsafe_allow_html=True)
        inputs = {
            'numero_identificacao': st.text_input("Número de Identificação", placeholder='Apenas Dígitos Numéricos'),
            'complete_name': st.text_input("Nome Completo", placeholder='Nome'),
            'date_nascimento': st.date_input("Data de Nascimento", min_value=datetime(1960, 1, 1), max_value=(datetime.now())).strftime('%Y-%m-%d'),
            'date_admissao': st.date_input("Data de Admissão", max_value=(datetime(datetime.today().year,12,31))).strftime('%Y-%m-%d'),
            'role': st.selectbox("Cargo", ["Padeiro", "Auxiliar de Padeiro", "Atendente de Caixa", "Cozinheira"]),
            'telephone_number': st.text_input("Telefone (85900000000)", placeholder="XXXXXXXXXXXXX"),
            'observation': st.text_area('Observações Adicionais', placeholder="Texto")}
        app_pass = st.text_input(label=":red[Senha]", type="password")
    
        # Validations
        is_identificacao_digit_correct = is_numeric_field(inputs['numero_identificacao'])
        is_6_digits_long = is_6_chars_long(inputs['numero_identificacao'])
        is_correct_password = is_authenticated_password(app_pass)
        is_ok_name = is_correct_name(inputs['complete_name'])
        is_valid_phone_number = validate_phone_number(inputs['telephone_number'])

        if app_pass == '':
            pass
        elif not is_correct_password:
            st.error('Senha Incorreta!')

        if inputs['numero_identificacao'] == '':
            pass
        elif not is_identificacao_digit_correct:
            st.error(
                "O número de identificação deve conter apenas dígitos numéricos.")
        elif not is_6_digits_long :
            st.error("O número de identificação deve ter exatamente 6 dígitos.")

        if not is_ok_name:
            st.error("Nome completo é obrigatório.")

        if inputs['telephone_number'] == '':
            pass
        elif not is_valid_phone_number:
            st.error('Telefone fornecido é inválido!')

        conditions_check = [is_identificacao_digit_correct,
                            is_correct_password,
                            is_ok_name,
                            is_6_digits_long,
                            is_valid_phone_number]

        if all(conditions_check):
            if st.button("Cadastrar"):
                user_inserted = self.user_controller.insert_employee(inputs,log_call=True)
                if isinstance(user_inserted, User):
                    st.success("Usuário adicionado com sucesso!")
                else:
                    st.error(
                        "Funcionário já cadastrado. Digite novo ID!", icon='🚩')


    def select_users(self):
        st.markdown('<h4 style="color:white;">Funcionários Cadastrados</h4>', unsafe_allow_html=True)
        choosen_columns = st.multiselect('Campos',
                                        options=['Número de Identificação',
                                                'Nome Completo', "Data de Admissão",
                                                "Status",'Data de Nascimento',
                                                "Cargo","Telefone", "Observação"])
        column_mapping = {
            'Número de Identificação': 'numero_identificacao',
            'Nome Completo': 'complete_name',
            'Data de Nascimento': 'date_nascimento',
            'Data de Admissão': 'date_admissao',
            'Cargo': 'role',
            'Telefone': 'telephone_number',
            'Observação': 'observation',
            'Status':'status'
        }
        database_columns = [column_mapping[column] for column in choosen_columns]
        inverted_mapping = {value: key for key, value in column_mapping.items()}

        if choosen_columns:
            if st.button("Consultar"):
                users = self.user_controller.select_info_employees(database_columns,log_call=True)
                user_struct = {}
                for column in database_columns:
                    user_struct[column] = [getattr(user, column) for user in users]
            
                df = pd.DataFrame(user_struct)

                if 'Número de Identificação' in choosen_columns:
                    df['numero_identificacao'] = df['numero_identificacao'].astype(str).str.zfill(6) 
    
                columns_to_convert = []
                if 'Data de Admissão' in choosen_columns:
                    columns_to_convert.append('date_admissao')
                if 'Data de Nascimento' in choosen_columns:
                    columns_to_convert.append('date_nascimento')

                df = brazilian_date(df, columns_to_convert)
                df.rename(columns=inverted_mapping, inplace=True)
                df.index.name = "Id"
                pretty_html_table(df)
        
    
    def updatestatus_users(self):
        st.markdown('<h4 style="color:white;">Status Funcionários</h4>', unsafe_allow_html=True)
        app_pass = st.text_input(label=":red[Senha]", type="password")
        is_correct_password = is_authenticated_password(app_pass)

        if app_pass == '':
            pass
        elif not is_correct_password:
            st.error('Senha Incorreta!')

        if is_correct_password:
            users = self.user_controller.select_info_employees(['numero_identificacao','complete_name','role','status','date_admissao'])
            for user in users:
                user_key = f"User {user.numero_identificacao}"
                with st.expander(f"{user.complete_name} (ID: {user.numero_identificacao:06d})"):
                    user_info_col = st.columns((2,2,1,1))
                    user_info_col[0].write(f"**Cargo:** {user.role}")
                    user_info_col[1].write(f"**Admissão:** {datetime.strftime(datetime.strptime(user.date_admissao,('%Y-%m-%d')),'%d-%m-%Y')}")
                    new_status = user_info_col[3].radio("**Status**", ["Ativo", "Inativo"], index=0 if user.status == "Ativo" else 1, key=f"toggle_{user_key}")
                    if new_status != user.status:
                        self.user_controller.update_employees_status(user.numero_identificacao, new_status == "Ativo", log_call=True)
                        st.success("Ateração Realizada")
                        time.sleep(1)
                        st.experimental_rerun()
                    


    def update_user(self):
        st.markdown('<h4 style="color:white;">Alteração de Cadastro</h4>', unsafe_allow_html=True)
        users = self.user_controller.select_info_employees(['numero_identificacao','complete_name'])
        user_names = [user.complete_name for user in users]
        selected_user = st.selectbox("Funcionário", user_names)
        user_id = users[user_names.index(selected_user)].numero_identificacao
        choosen_columns = st.multiselect("Campos", options=[
                                                            'Nome Completo',"Data de Nascimento",
                                                            "Data de Admissão","Cargo",
                                                            "Telefone", "Observação"])

        column_input_type = {
        'Número de Identificação': st.text_input,
        'Nome Completo': st.text_input,
        'Data de Nascimento': st.date_input,
        'Data de Admissão': st.date_input,
        'Cargo': st.selectbox,
        'Telefone': st.text_input,
        'Observação': st.text_input,
}
        column_mapping = {
            'Número de Identificação': 'numero_identificacao',
            'Nome Completo': 'complete_name',
            'Data de Nascimento': 'date_nascimento',
            'Data de Admissão': 'date_admissao',    
            'Cargo': 'role',
            'Telefone': 'telephone_number',
            'Observação': 'observation',
        }
        
        cargo_choices = ["Padeiro", "Auxiliar de Padeiro", "Atendente de Caixa", "Cozinheira"] # Provide appropriate cargo choices here


        if len(choosen_columns) == 0:
            pass
        else:
            st.markdown('<h4 style="color:white;">Atualizando</h4>',unsafe_allow_html=True)  
            database_columns = []
            for column in choosen_columns:
                if column == 'Cargo':
                    database_columns.append((column_mapping[column], column_input_type[column](f"{column}", options=cargo_choices)))
                else:
                    database_columns.append((column_mapping[column], column_input_type[column](f"{column}")))

            app_pass = st.text_input(label=":red[Senha]", type="password")
            is_correct_password = is_authenticated_password(app_pass)
            if app_pass == '':
                pass
            elif not is_correct_password:
                st.error('Senha Incorreta!')

            if is_correct_password:
                if st.button("Alterar Cadastro"):
                    returned_user = self.user_controller.update_employee(database_columns,user_id,log_call=True)
                    name = returned_user.complete_name
                    st.success(f"As informações de {name} foram atualizadas")
                    time.sleep(2)
                    st.experimental_rerun()
    