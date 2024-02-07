import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import smtplib
import email.message
import re
import base64

load_dotenv()
gmail_username = os.getenv('GMAIL_USERNAME')
app_password = os.getenv('APP_PASSWORD')

companies = [
    { 'name': 'Core Loop', 'url': 'https://coreloop.ai/#careers', 'status': 'not applied' },
    { 'name': 'Core Loop2', 'url': 'https://coreloop.ai/#careers', 'status': 'applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_2', 'status': 'not applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_3', 'status': 'not applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_4', 'status': 'not applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_5', 'status': 'not applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_6', 'status': 'not applied' },
    # { 'name': '', 'url': 'URL_DA_PAGINA_7', 'status': 'not applied' },
  ]

palavras_chave = ['Concept Artist', 'Artist', '2D', 'Game Designer', 'Prop Artist', 'Character Artist', 'Environment Artist', 'UX Designer', 'UI Designer', 'Level Designer', 'Game Artist', 'Game Art', 'Game Artist', 'Game Art', 'Designer']

open_job_list = []
image_path = "img/me.png"

def assemble_email():
    with open("index.html", "r") as file:
        email_html = file.read()

    insertion_index = email_html.find("<!-- JOB CONTENT -->")

    job_content = ""

    for job in open_job_list:
        job_content += f"""
        <table
            style="font-family:arial,helvetica,sans-serif;"
            role="presentation" cellpadding="0"
            cellspacing="0" width="100%"
            border="0">
            <tbody>
                <tr>
                <td
                    style="overflow-wrap:break-word;word-break:break-word;padding:27px 27px 10px;font-family:arial,helvetica,sans-serif;"
                    align="left">
                    <h1
                    style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-size: 19px; font-weight: 400;">
                    <span><span><span><strong>Vaga
                            Aberta na
                            {job['name']}</strong></span></span></span>
                    </h1>
                </td>
                </tr>
            </tbody>
            </table>

            <table
            style="font-family:arial,helvetica,sans-serif;"
            role="presentation" cellpadding="0"
            cellspacing="0" width="100%"
            border="0">
            <tbody>
                <tr>
                <td
                    style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;"
                    align="left">
                    <div align="center">
                    <a href="{job['url']}" target="_blank"
                        class="v-button"
                        style="box-sizing: border-box;display: inline-block;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; border-radius: 4px;-webkit-border-radius: 4px; -moz-border-radius: 4px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;font-size: 14px;
                        background-image: linear-gradient(to right, #23d1fd, #b524ff);">
                        <span style="display:block;padding:10px 20px;line-height:120%;">
                            <span style="line-height: 16.8px;">Clique aqui para ver a vaga!</span>
                        </span>
                    </a>
                </div>
                </td>
                </tr>
            </tbody>
            </table>
        """
    email_html = email_html[:insertion_index] + job_content + email_html[insertion_index:]

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
    if search_keywords_in_url(company['url'], palavras_chave) and company['status'] == 'not applied':
        open_job_list.append(company)
    else:
        print("Palavras-chave não encontradas em " + company['name'] + " no link " + company['url'])

if(len(open_job_list) > 0):
    send_email()
else:
    print("Nenhuma vaga encontrada")