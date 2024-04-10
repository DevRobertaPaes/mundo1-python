import tkinter as tk
from PIL import Image, ImageTk
import os
import Main as Main

class Alunos():
    def __init__(self):
        # Lista de alunos
        self.alunos = [
            "Roberta Coutinho Paes - Matrícula 202307274356",
            "Rubia Rafaela Nascimento Hilario - Matrícula 202003423769",
            
        ]
        # Formate os nomes dos alunos
        self.nomes_formatados = "\n".join(self.alunos)
        
        # Crie a janela da nova página
        self.page2_window = tk.Tk()
        self.page2_window.title("Missão Certificação 1, 03/2023")
        
        # Defina o tamanho da janela para 1920x1080 pixels
        self.window_width = 700
        self.window_height = 400
        self.page2_window.geometry(f"{self.window_width}x{self.window_height}")
        
        # Configure a cor de fundo
        self.bgcolor = '#17202A'
        self.page2_window.configure(bg=self.bgcolor)
        
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(self.current_directory, 'logo_estacio.png')
        
        # Carregue o logotipo da Estácio localizado em "logo_estacio.png"
        self.logo_image = Image.open(self.logo_path)  # Use "r" antes do caminho para interpretá-lo como uma string crua
        self.logo_image = self.logo_image.resize((100, 50))  # Redimensione o logotipo
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        # Crie um rótulo para o logotipo
        self.logo_label = tk.Label(self.page2_window, image=self.logo_photo, bg=self.bgcolor)
        self.logo_label.grid(row=0, column=0, padx=(self.window_width-700) /2, pady=10, rowspan=1)  # Posicione à esquerda e ocupe duas linhas
        
        # Crie um rótulo para o cabeçalho "Dev Team 19" no centro da página
        self.cabecalho_label = tk.Label(self.page2_window, text="Dev Team 19", bg=self.bgcolor, fg="white", font=("Roboto", 16))
        self.cabecalho_label.grid(row=2, column=2, padx=(self.window_width-700) /2, pady=13, columnspan=8)
        
        # Crie os dizeres formatados no centro da página com texto branco e fundo preto
        self.dizeres_label = tk.Label(self.page2_window, text=self.nomes_formatados, bg=self.bgcolor, fg="white", font=("Roboto", 12))
        self.dizeres_label.grid(row=3, column=3, padx=(self.window_width-700)/2, pady=15, columnspan=6)
        
        self.back_button = tk.Button(self.page2_window, text='Voltar', command=self.back_to_login, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        self.back_button.grid(row=4, column=5, columnspan=2, pady=30)

        self.page2_window.mainloop()
        
    def back_to_login(self):
        self.page2_window.destroy()
        Main.Main()
    
