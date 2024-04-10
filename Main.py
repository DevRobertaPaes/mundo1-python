import tkinter as tk
from CTkMessagebox import CTkMessagebox
import Auth as Auth
import HomePage as Home
import Alunos as Alunos

class Main():

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title('Login')
        self.login_window.geometry('280x400')
        self.login_window.resizable(False, False)
        self.login_window.configure(bg='#17202A')

        self.welcome_label = tk.Label(self.login_window, text='Bem Vindo', anchor='center', bg='#17202A', foreground='#48C9B0', font=('Calibri', 18))
        self.welcome_label.grid(row=0, column=1, columnspan=2, pady=20, padx=10, sticky='n')
        
        self.login_label = tk.Label(self.login_window, text="Usuário:", bg='#17202A', foreground='white', font=("Calibri", 12))
        self.login_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.login_entry = tk.Entry(self.login_window, bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        self.login_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        self.password_label = tk.Label(self.login_window, text="Senha:", bg="#17202A", foreground='white', font=("Calibri", 12))
        self.password_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.login_window, show="*", bg="#303030", foreground='white', font=("Calibri", 12), width=14, bd=0, relief='solid')
        self.password_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        
        login_button = tk.Button(self.login_window, text="Login", command=self.login, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        login_button.grid(row=3, column=1, columnspan=2, pady=20)

        alunos_button = tk.Button(self.login_window, text="Alunos", command=self.alunos, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        alunos_button.grid(row=4, column=1, columnspan=2, pady=20)

        exit_button = tk.Button(self.login_window, text="Sair", command=self.exit, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        exit_button.grid(row=5, column=1, columnspan=2, pady=20)
        
        self.login_window.mainloop()

    
    def login(self):
        self.username = self.login_entry.get()
        verifyUser = Auth.authenticateUser(self.login_entry.get(), self.password_entry.get())
        if verifyUser == True:
            self.login_window.destroy()
        
            open_home_page = Home.HomePage(username=self.username)
            open_home_page.mainloop()
        else:
            CTkMessagebox(title='Erro ao fazer o login', message='Usuário ou senha incorretos', icon='cancel', width=280)
    
    def alunos(self):
        self.login_window.destroy()
        Alunos.Alunos()
    
    def exit(self):
        self.login_window.destroy()
        

        


if __name__ == '__main__':
    app = Main()
    app.login_window.mainloop()
