import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar
import paho.mqtt.client as mqtt
from datetime import datetime

class MqttSubscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Subscriber App")

        mqttBroker = "broker.emqx.io"
        self.client = mqtt.Client("Smartphone")
        self.client.on_message = self.on_message
        self.client.connect(mqttBroker)
        self.client.loop_start()

        self.last_messages = {}

        self.create_widgets()

        # Adiciona um botão para abrir a nova janela de feed
        open_feed_button = tk.Button(self.root, text="Abrir Feed", command=self.open_feed_window)
        open_feed_button.pack()

        # Estrutura para armazenar mensagens passadas
        self.past_messages = []

    def create_widgets(self):
        # Criação de widgets para o novo tópico
        new_topic_label = tk.Label(self.root, text="Novo Tópico")
        new_topic_label.pack()
        self.new_topic_entry = tk.Entry(self.root)
        self.new_topic_entry.pack()

        subscribe_button = tk.Button(self.root, text="Assinar", command=self.subscribe_new_topic)
        subscribe_button.pack()

        self.create_topic_frame("DOLAR", "Cotacao Dolar")
        self.create_topic_frame("EURO", "Cotacao Euro")
        self.create_topic_frame("TEMPFOZ", "Temperatura Foz")

    def create_topic_frame(self, topic, topic_text):
        frame = tk.Frame(self.root)
        frame.pack()

        topic_var = tk.BooleanVar()
        tk.Checkbutton(frame, text=topic_text, variable=topic_var, command=lambda: self.subscribe_topic(topic, topic_var), width=15).pack(side=tk.LEFT)

        timestamp_label = tk.Label(frame, text="", width=10)
        timestamp_label.pack(side=tk.LEFT)

        last_message_entry = tk.Entry(frame, font=("Arial", 12), width=13, state='readonly')
        last_message_entry.pack(side=tk.LEFT)

        self.last_messages[topic] = {"entry": last_message_entry, "timestamp_label": timestamp_label}

    def subscribe_topic(self, topic, topic_var):
        if topic_var.get():
            self.client.subscribe(topic)
        else:
            self.client.unsubscribe(topic)

    def subscribe_new_topic(self):
        new_topic = self.new_topic_entry.get()
        if new_topic:
            self.create_topic_frame(new_topic, new_topic)
            self.client.subscribe(new_topic)

            self.new_topic_entry.delete(0, tk.END)
        else:
            print("Por favor, insira o nome do novo tópico.")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = str(message.payload.decode("utf-8"))
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Armazena a mensagem na lista de mensagens passadas
        self.past_messages.append(f"[{timestamp}] {topic}: {payload}")

        # Atualiza o timestamp e a caixa de texto com a última mensagem recebida
        if topic in self.last_messages:
            self.last_messages[topic]["timestamp_label"].config(text=timestamp)
            self.last_messages[topic]["entry"].configure(state='normal')
            self.last_messages[topic]["entry"].delete(0, tk.END)
            self.last_messages[topic]["entry"].insert(tk.END, payload)
            self.last_messages[topic]["entry"].configure(state='readonly')

        # Adiciona a mensagem à caixa de texto do feed
        if hasattr(self, 'feed_text'):
            self.feed_text.configure(state='normal')
            self.feed_text.insert(tk.END, f"[{timestamp}] {topic}: {payload}\n")
            self.feed_text.configure(state='disabled')
    
    def open_feed_window(self):
        feed_window = Toplevel(self.root)
        feed_window.title("Feed de Mensagens")

        # Adiciona uma caixa de texto para mostrar as mensagens
        self.feed_text = Text(feed_window, wrap="word", state="disabled")
        self.feed_text.pack(expand=True, fill="both")

        # Adiciona uma barra de rolagem para a caixa de texto
        scrollbar = Scrollbar(feed_window, command=self.feed_text.yview)
        scrollbar.pack(side="right", fill="y")

        # Conecta a barra de rolagem à caixa de texto
        self.feed_text.config(yscrollcommand=scrollbar.set)

        # Exibe as mensagens passadas no feed
        for past_message in self.past_messages:
            self.feed_text.configure(state='normal')
            self.feed_text.insert(tk.END, f"{past_message}\n")
            self.feed_text.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x250")
    app = MqttSubscriberApp(root)
    root.mainloop()
