import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import smtplib

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

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')

def send_email():
    servidor_email = smtplib.SMTP('smtp.gmail.com', port)
    servidor_email.starttls()
    servidor_email.login(username, password)
    remetente = 'jobservicebot@gmail.com'
    destinatarios = ['jobservicebot@gmail.com']
    conteudo = 'Olá, este é um email de teste.'
    servidor_email.sendmail(remetente, destinatarios, conteudo)

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
        send_email()
        print("ALERTA DE VAGA em " + company['name'] + " no link " + company['url'])
        # add to a list and send them all in only one report email
        # send_whatsapp_alert("ALERTA DE VAGA em " + company['name'] + " no link " + company['url'])
    else:
        print("Palavras-chave não encontradas em " + company['name'] + " no link " + company['url'])