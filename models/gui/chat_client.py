# gui/chat_client.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from menu_config import create_menu
from text_to_speech import TextToSpeech
import requests
import json

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Cliente de Chat RAG")
        master.geometry("800x800")
        
        # Tema escuro inicial
        self.bg_color = "#2E2E2E"  # Cor de fundo escura
        self.text_color = "#FFFFFF"  # Texto branco
        master.configure(bg=self.bg_color)

        # Inicializa o TTS
        self.tts = TextToSpeech()

        # Cria o menu superior
        create_menu(master, self)

        # Frame para entrada e botão
        self.input_frame = tk.Frame(master, bg=self.bg_color)
        self.input_frame.pack(padx=10, pady=10)

        # Campo de entrada
        self.entry = tk.Entry(self.input_frame, width=60, font=("Roboto", 12), bg="#1C1C1C", fg=self.text_color, insertbackground=self.text_color)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message_event)

        # Botão de enviar
        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.send_message, font=("Roboto", 12), bg="#3A3A3A", fg=self.text_color)
        self.send_button.pack(side=tk.LEFT)

        # Área de exibição de mensagens
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=25, state='disabled', font=("Roboto", 12), bg="#1C1C1C", fg=self.text_color)
        self.chat_area.pack(padx=10, pady=10)

        # Indicador de fala
        self.speaking_label = tk.Label(master, text="", fg="green", font=("Roboto", 10, "italic"), bg=self.bg_color)
        self.speaking_label.pack()

        # URL do backend
        self.api_url = 'http://192.168.56.1:8000/ask'  # Atualize conforme necessário

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showwarning("Entrada Vazia", "Por favor, digite uma pergunta.")
            return

        # Adicionar mensagem do usuário ao chat
        self.append_message("Você", user_input)

        # Limpar campo de entrada
        self.entry.delete(0, tk.END)

        # Enviar requisição ao backend em uma thread separada para não bloquear a GUI
        threading.Thread(target=self.send_request, args=(user_input,)).start()

    def send_request(self, user_input):
        try:
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'question': user_input})
            )

            if response.status_code == 200:
                response_body = response.content.decode('utf-8')
                data = json.loads(response_body)
                reply = data.get('response', 'Nenhuma resposta recebida.')
                self.append_message("Assistente", reply)
                self.tts.speak(reply)  # Fala a resposta usando TTS
            else:
                self.append_message("Assistente", "Erro ao obter a resposta.")
        except requests.exceptions.RequestException as e:
            self.append_message("Assistente", "Erro de conexão com o servidor.")

    def append_message(self, sender, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)  # Auto-scroll para a última mensagem

    def toggle_theme(self):
        # Alterna entre o tema claro e escuro
        if self.bg_color == "#2E2E2E":  # Tema escuro
            self.bg_color = "#FFFFFF"
            self.text_color = "#000000"
        else:  # Tema claro
            self.bg_color = "#2E2E2E"
            self.text_color = "#FFFFFF"
        
        # Aplica o tema atualizado
        self.master.configure(bg=self.bg_color)
        self.input_frame.configure(bg=self.bg_color)
        self.chat_area.configure(bg="#1C1C1C" if self.bg_color == "#2E2E2E" else "#F0F0F0", fg=self.text_color)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
