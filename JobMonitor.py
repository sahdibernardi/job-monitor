import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from twilio.rest import Client

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
twilio_sid = os.getenv('TWILIO_SID')
twilio_token = os.getenv('TWILIO_TOKEN')
twilio_numero_de = os.getenv('TWILIO_PHONE_FROM')
twilio_numero_para = os.getenv('TWILIO_PHONE_TO')

def send_whatsapp_alert(mensagem):
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=mensagem,
        from_=twilio_numero_de,
        to=twilio_numero_para
    )
    print("Mensagem enviada:", message.sid)

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
        send_whatsapp_alert("ALERTA DE VAGA em " + company['name'] + " no link " + company['url'])
    else:
        print("Palavras-chave não encontradas em " + company['name'] + " no link " + company['url'])
