import threading
import paho.mqtt.client as mqtt
import time
import requests

def obter_cotacao_moeda(url, topico_mqtt):
    mqttBroker = "broker.emqx.io"
    client = mqtt.Client(topico_mqtt)
    client.connect(mqttBroker)

    while True:
        # Fazendo a requisição GET
        response = requests.get(url)

        # Verificando se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # A resposta da API está em formato JSON, você pode acessar os dados assim:
            data = response.json()

            valor = data.get('brl')

            # Agora você pode manipular os dados como desejar
            print("{}: {}".format(topico_mqtt, valor))

            client.publish(topico_mqtt, valor)
            print("Just published " + str(valor) + " to Topic " + topico_mqtt)
        else:
            print("Falha na requisição. Código de status:", response.status_code)

        time.sleep(10)

def obter_temp(url, topico_mqtt):
    mqttBroker = "broker.emqx.io"
    client = mqtt.Client(topico_mqtt)
    client.connect(mqttBroker)

    while True:
        # Fazendo a requisição GET
        response = requests.get(url)

        # Verificando se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # A resposta da API está em formato JSON, você pode acessar os dados assim:
            data = response.json()

            valor = data.get('results').get('temp')

            # Agora você pode manipular os dados como desejar
            print("{}: {}".format(topico_mqtt, valor))

            client.publish(topico_mqtt, valor)
            print("Just published " + str(valor) + " to Topic " + topico_mqtt)
        else:
            print("Falha na requisição. Código de status:", response.status_code)

        time.sleep(15)

# Criando threads para as funções obter_cotacao_dolar e obter_cotacao_euro
thread_cotacao_dolar = threading.Thread(target=obter_cotacao_moeda, args=("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd/brl.json", "DOLAR"))
thread_cotacao_euro = threading.Thread(target=obter_cotacao_moeda, args=("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur/brl.json", "EURO"))
thread_temp_foz = threading.Thread(target=obter_temp, args=("https://api.hgbrasil.com/weather?key=a763f2d7&woeid=455862", "TEMPFOZ"))

# Iniciando as threads
thread_cotacao_dolar.start()
thread_cotacao_euro.start()
thread_temp_foz.start()