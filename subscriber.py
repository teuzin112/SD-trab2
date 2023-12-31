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
        self.feed_window = None

        self.create_widgets()

    def create_widgets(self):
        # Botão para abrir a nova janela de feed
        feed_button = tk.Button(self.root, text="Abrir Feed", command=self.open_feed_window)
        feed_button.pack()

        # Criação de widgets para novo tópico
        new_topic_label = tk.Label(self.root, text="Novo Tópico")
        new_topic_label.pack()
        self.new_topic_entry = tk.Entry(self.root)
        self.new_topic_entry.pack()

        subscribe_button = tk.Button(self.root, text="Assinar", command=self.subscribe_new_topic)
        subscribe_button.pack()

        self.create_topic_frame("DOLAR", "Cotacao Dolar")
        self.create_topic_frame("EURO", "Cotacao Euro")
        self.create_topic_frame("TEMPFOZ", "Temperatura Foz")

    def open_feed_window(self):
        self.feed_window = Toplevel(self.root)
        self.feed_window.title("Feed")
        
        feed_text = Text(self.feed_window, wrap=tk.WORD, width=30, height=10)
        feed_text.pack(padx=10, pady=10)

        scrollbar = Scrollbar(self.feed_window, command=feed_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        feed_text.config(yscrollcommand=scrollbar.set)

        self.feed_text = feed_text

    def create_topic_frame(self, topic, topic_text):
        frame = tk.Frame(self.root)
        frame.pack()

        # gambiarrazinha
        topic_var = tk.BooleanVar()
        if(topic not in ['DOLAR', 'EURO', 'TEMPFOZ']):
            topic_var.set(True)
        
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

        # Atualiza o timestamp e a caixa de texto com a última mensagem recebida
        if topic in self.last_messages:
            self.last_messages[topic]["timestamp_label"].config(text=timestamp)
            self.last_messages[topic]["entry"].configure(state='normal')
            self.last_messages[topic]["entry"].delete(0, tk.END)
            self.last_messages[topic]["entry"].insert(tk.END, payload)
            self.last_messages[topic]["entry"].configure(state='readonly')

            # Adiciona a mensagem à caixa de texto do feed
            if hasattr(self, 'feed_text') and self.feed_text.winfo_exists():
                self.feed_text.insert(tk.END, f"[{timestamp}] {topic}: {payload}\n")
                self.feed_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x250")
    app = MqttSubscriberApp(root)
    root.mainloop()
