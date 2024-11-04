# gui/menu_config.py

import tkinter as tk
from tkinter import messagebox

def create_menu(master, client):
    menu_bar = tk.Menu(master, bg=client.bg_color, fg=client.text_color)

    # Menu de Opções
    options_menu = tk.Menu(menu_bar, tearoff=0, bg=client.bg_color, fg=client.text_color)
    options_menu.add_command(label="Mudar Tema", command=client.toggle_theme)
    options_menu.add_command(label="Configurações", command=show_settings)
    options_menu.add_command(label="Sobre", command=show_about)

    menu_bar.add_cascade(label="Opções", menu=options_menu)
    master.config(menu=menu_bar)

def show_settings():
    messagebox.showinfo("Configurações", "Configurações ainda não disponíveis.")

def show_about():
    messagebox.showinfo("Sobre", "Cliente de Chat RAG - Versão 1.0\nDesenvolvido por [Seu Nome]")
