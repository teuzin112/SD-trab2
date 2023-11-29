import tkinter as tk
import paho.mqtt.client as mqtt

def enviar_aviso():
    topico = topico_entry.get()
    mensagem = mensagem_entry.get()
    
    if topico and mensagem:
        client.publish(topico, mensagem)
        mensagem_entry.delete(0, tk.END)

        resultado_label.config(text=f"Just published {mensagem} to Topic {topico}")
    else:
        resultado_label.config(text="Por favor, preencha ambos os campos.")

mqttBroker = "broker.emqx.io"
client = mqtt.Client("aviso")
client.connect(mqttBroker)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Envio de Aviso MQTT")

# Widgets
topico_label = tk.Label(root, text="Tópico:")
topico_entry = tk.Entry(root)

mensagem_label = tk.Label(root, text="Mensagem:")
mensagem_entry = tk.Entry(root)

enviar_button = tk.Button(root, text="Enviar Aviso", command=enviar_aviso)

resultado_label = tk.Label(root, text="")

# Layout
topico_label.grid(row=0, column=0, padx=10, pady=5)
topico_entry.grid(row=0, column=1, padx=10, pady=5)

mensagem_label.grid(row=1, column=0, padx=10, pady=5)
mensagem_entry.grid(row=1, column=1, padx=10, pady=5)

enviar_button.grid(row=2, column=0, columnspan=2, pady=10)

resultado_label.grid(row=3, column=0, columnspan=2, pady=5)

# Executa a interface gráfica
root.mainloop()
