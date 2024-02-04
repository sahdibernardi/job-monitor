import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from twilio.rest import Client
from mailchimp_marketing import Client

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
mailchimp = Client()

url_mailchimp = os.getenv('MAILCHIMP_URL')
mailchimp_api_key = os.getenv('MAILCHIMP_API_KEY')
mailchimp_dc = os.getenv('MAILCHIMP_DC')
recipient_email = os.getenv('MAILCHIMP_RECIPIENT_EMAIL')

mailchimp.set_config({
  "api_key": mailchimp_api_key,
  "server": mailchimp_dc
})

data = {
    "email_address": recipient_email,
    "content": {
        "html": "<p>Conteúdo HTML personalizado do email</p>",
        "text": "ALERTA DE VAGAS!"
    }
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {mailchimp_api_key}'
}

def send_mailchimp_email(mensagem):
  response = requests.post(url, json=data, headers=headers)
  if response.status_code == 200:
      print("Email enviado com sucesso para:", recipient_email)
  else:
      print("Erro ao enviar email:", response.text)


#Twilio
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

def mailchimp_connection_test():
  # preciso que crie uma campanha apenas na primeira vez. Depois, só atualize o conteúdo e envie o email
  # response = mailchimp.campaigns.create({"type": "regular"})
  # response = mailchimp.campaigns.update("44cd652a74", {"social_card": { "title": "Campanha legal", "description": "Descrição legal"}})
  response = mailchimp.campaigns.list()
  print(response)

for company in companies:
    if search_keywords_in_url(company['url'], palavras_chave):
      mailchimp_connection_test()
      print("ALERTA DE VAGA em " + company['name'] + " no link " + company['url'])
        # add to a list and send them all in only one report email
        # send_whatsapp_alert("ALERTA DE VAGA em " + company['name'] + " no link " + company['url'])
    else:
        print("Palavras-chave não encontradas em " + company['name'] + " no link " + company['url'])
