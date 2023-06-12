import smtplib
import pandas as pd
import streamlit as st
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



def send_email(df,selected_month_pt):
    # Create a BytesIO object, save the Excel file in memory
    df = df.reindex(columns= ['Data','Nome'] + ["Entrada", "Entrada Almoço", "Saída Almoço", "Saída"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         for name in df['Nome'].unique():
            employee_df = df[df['Nome'] == name].copy()
            employee_df.to_excel(writer, index=False, sheet_name=name)
    output.seek(0) 

    #Mail
    msg = MIMEMultipart()
    msg['From'] = st.secrets['email']
    msg['To'] = st.secrets['email']
    msg['Subject'] = 'Relatório de frequência dos funcionários'

    body = 'Segue ponto de funcionários do período ' + selected_month_pt
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEApplication(output.read(), Name='attendance_report.xlsx')
    part['Content-Disposition'] = f'attachment; filename="Ponto de Funcionarios ({selected_month_pt}).xlsx"'
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(msg['From'],st.secrets['email-pass'])
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()
        st.success('Email enviado!')
    except Exception as e:
        st.error(f'Falar ao enviar o email: {e}')
