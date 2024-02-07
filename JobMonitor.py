import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import smtplib
import email.message

load_dotenv()
gmail_username = os.getenv('GMAIL_USERNAME')
app_password = os.getenv('APP_PASSWORD')

companies = [
  { 'name': 'Core Loop', 'url': 'https://coreloop.ai/#careers' },
  # { 'name': '', 'url': 'URL_DA_PAGINA_2' },
  # { 'name': '', 'url': 'URL_DA_PAGINA_3' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_4' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_5' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_6' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_7' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_8' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_9' }
  # { 'name': '', 'url': 'URL_DA_PAGINA_10' }
  ]

palavras_chave = ['Concept Artist', 'Artist', '2D', 'Game Designer', 'Prop Artist', 'Character Artist', 'Environment Artist', 'UX Designer', 'UI Designer', 'Level Designer', 'Game Artist', 'Game Art', 'Game Artist', 'Game Art', 'Designer']

open_job_list = []
image_path = "img/me.png"

def assemble_email():
    email_html = """
    <html>
    <head>
    <style>
    .job-link {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    </style>
    </head>
    <body>
    <p>Alerta de vagas:</p>
    """

    for job in open_job_list:
        email_html += f"""
        <p>Vaga disponível em {job['name']}</p>
        <a class="job-link" href="{job['url']}">Ver a vaga</a>
        """

    email_html += """
    </body>
    </html>
    """

    return email_html

def send_email():
    email_html = assemble_email()

    msg = email.message.Message()
    msg['Subject'] = "Teste de Email"
    msg['From'] = gmail_username
    msg['To'] = gmail_username
    password = app_password
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_html)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

def search_keywords_in_url(url, palavras_chave):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    texto = soup.get_text()
    for palavra in palavras_chave:
        if palavra in texto:
            return True
    return False

for company in companies:
    if search_keywords_in_url(company['url'], palavras_chave):
        open_job_list.append(company)
    else:
        print("Palavras-chave não encontradas em " + company['name'] + " no link " + company['url'])

if(len(open_job_list) > 0):
    send_email()
else:
    print("Nenhuma vaga encontrada")