import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import pandas as pd
import EntryFocus as Focus
import os
import Main as Main

class HomePage(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title('HOME PAGE')
        self.geometry('880x600')
        self.username = username

        self.bar = tk.Frame(self, bg='#273746', width=200)
        self.bar.pack(side=tk.LEFT, fill=tk.Y)

        self.switch_case = {
            'admin': {
                'Início': InicioPage,
                'Sistemas': SistemasPage,
                'Perfis de Acesso': PerfisPage,
                'Matriz SoD': MatrizPage,
                'Usuários': UsuariosPage,
                'Alunos': AlunosPage,
            },
            'aluno': {
                'Início': InicioPage,
                'Alunos': AlunosPage
            },
        }

        self.pages = self.switch_case[self.username]

        self.options = []
        for page, _ in self.pages.items():
            self.options.append(page)

        for item in self.options:
            self.btn = tk.Button(self.bar, text=item, command=lambda text=item: self.show_button(text), foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
            self.btn.pack(pady=10, padx=10)

        self.main_content = tk.Frame(self, bg='#273746')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.back_button = tk.Button(self.bar, text='Log Out', command=self.back_to_login, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        self.back_button.pack(pady=10, padx=10)


        self.show_page('Início')

    def show_button(self, button_text):
        self.show_page(button_text)

    def show_page(self, page_name):
        if page_name in self.pages:
            page = self.pages[page_name]()
            if isinstance(page, tk.Frame):
                if self.main_content:
                    self.main_content.destroy()
                self.main_content = page
                self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
    def back_to_login(self):
        self.destroy()
        Main.Main()



class InicioPage(tk.Frame):
    def __init__(self):
        super().__init__()

        self.title = ("Gestão Eficiente de Perfis de Acesso Corporativo:\nPrevenção de Conflitos e Segurança de Dados\n")
        self.content = (
            "Este projeto foi desenvolvido  para o controle interno de uma empresa\ne é responsável por analisar os perfis de acessos de seus funcionários\nem seu sistema e verificar se a combinação de perfis, para um\nmesmo usuário, pode apresentar algum conflito de interesse.\n",
            "Um conflito de interesse é quando o usuário pode se aproveitar dos acessos\nque possui para praticar uma fraude."
            )
        self.color = '#17202A'

        title_label = tk.Label(self, text=self.title, font=('Roboto', 17), foreground='#48C9B0', bg=self.color)
        title_label.pack(padx=20, pady=20)

        self.configure(bg=self.color)
        for line in self.content:
            label = tk.Label(self, text=line, font=('Roboto', 13), foreground='white', bg=self.color)
            label.pack(padx=20, pady=5)


class SistemasPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'systems.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.bg_color = '#17202A'

        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(expand=True, fill='both')

        self.title = tk.Label(frame, text='Cadastro de Sistemas', font=('Roboto', 16), foreground='#48C9B0', background=self.bg_color)
        self.title.pack(padx=20, pady=20)
        self.columns = ('Código do Sistema', 'Nome do Sistema')
        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=160)

        self.tree.pack(expand=True)

        self.code_entry = tk.Entry(frame, width=30, borderwidth=0, highlightthickness=0, bg='#273746', font=('Calibri', 12), justify='center')
        self.name_entry = tk.Entry(frame, width=30, borderwidth=0, highlightthickness=0, bg='#273746', font=('Calibri', 12), justify='center')

        self.code_placeholder = 'Insira o Código do Sistema'
        self.name_placeholder = 'Insira o Nome do Sistema'

        Focus.setup_entry(self.code_entry, self.code_placeholder)
        Focus.setup_entry(self.name_entry, self.name_placeholder)

        add_button = tk.Button(frame, text='Adicionar', command=self.add_system, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        remove_button = tk.Button(frame, text='Remover', command=self.remove_system, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)

        self.code_entry.pack(pady=10)
        self.name_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()
    

    def add_system(self):
        code = self.code_entry.get()
        name = self.name_entry.get()
        data = self.read_from_xlsx_systems()
        try:
            int(code)
        except:
            tkMessageBox.showerror('INVALID DATA', 'O código deve ser um número!')

        if int(code) in data:
            tkMessageBox.showerror('UNAUTHORIZED', 'O código inserido já existe.\nInsira outro código.')
        else:
            data[int(code)] = name
            if name == self.name_placeholder or name == '':
                tkMessageBox.showerror('INVALID DATA', 'Você deve inserir um\nnome para o sistema.')
            else:
                self.write_to_xlsx_systems(data)
                if code and name:
                    self.tree.insert('', 'end', values=(code, name))
                    self.code_entry.delete(0, 'end')
                    self.name_entry.delete(0, 'end')
                    if code == self.code_placeholder:
                        self.code_entry.insert(0, self.code_placeholder)
                        self.code_entry.configure(fg='#ABB2B9')
                    if name == self.name_placeholder:
                        self.name_entry.insert(0, self.name_placeholder)
                        self.name_entry.configure(fg='#ABB2B9')

    def remove_system(self):
        selected_item = self.tree.selection()

        if selected_item:
            code = str(self.tree.item(selected_item, 'values')[0])
            data = self.read_from_xlsx_systems()

            if int(code) in data:
                del data[int(code)]
                self.write_to_xlsx_systems(data)
                self.tree.delete(selected_item)
            else:
                tkMessageBox.showerror('NOT FOUND.', f'Esse código não foi\nencontrado no arquivo.')
    
    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_systems({})

        data = self.read_from_xlsx_systems()
        for code, name in data.items():
            self.tree.insert('', 'end', values=(code, name))
    
    def write_to_xlsx_systems(self, data):
        df = pd.DataFrame(list(data.items()), columns=self.columns)
        df.to_excel(self.filename, index=False)
        
    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}


class PerfisPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'profiles.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.bg_color = '#17202A'

        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(expand=True, fill='both')

        self.title = tk.Label(frame, text='Cadastro de Perfis de Acesso', font=('Roboto', 16), foreground='#48C9B0', background=self.bg_color)
        self.title.pack(padx=20, pady=20)
        self.columns = ('Código do Sistema', 'Nome do Perfil', 'Descrição')
        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=150)

        self.tree.pack(pady=20, expand=True)

        self.code = self.create_system_list()
        self.code_entry = tk.StringVar(self)
        self.code_entry.set(self.code[0])
        code_entry_dropdown = ttk.Combobox(frame, textvariable=self.code_entry, values=self.code, foreground='black', font=('Roboto', 14), width=15, justify='center')
        code_entry_dropdown.pack(pady=10)

        self.name_entry = tk.Entry(frame, width=30, borderwidth=0, highlightthickness=0, bg='#273746', font=('Calibri', 12), justify='center')
        self.description_entry = tk.Entry(frame, width=30, borderwidth=0, highlightthickness=0, bg='#273746', font=('Calibri', 12), justify='center')

        self.name_placeholder = 'Insira o Nome do Perfil'
        self.description_placeholder = 'Insira a Descrição'

        Focus.setup_entry(self.name_entry, self.name_placeholder)
        Focus.setup_entry(self.description_entry, self.description_placeholder)

        add_button = tk.Button(frame, text='Adicionar', command=self.add_profile, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        remove_button = tk.Button(frame, text='Remover', command=self.remove_profile, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)

        self.name_entry.pack(pady=10)
        self.description_entry.pack(pady=10)
        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()

    def create_system_list(self):
        systems_data = self.read_from_xlsx_systems()

        system_list = []
        for _, name in systems_data.items():
            system_list.append(name)
        
        return system_list

    def add_profile(self):
        code = self.code_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        
        data = self.read_from_xlsx_profiles()
        if name == self.name_placeholder or name == '':
            tkMessageBox.showerror('INVALID DATA', 'Você deve inserir\num nome\npara o perfil.')
        elif description == self.description_placeholder or description == '':
            tkMessageBox.showerror('INVALID DATA', 'Você deve inserir\numa descrição\npara o perfil.')
        else: 
            new_profile = {"code": code, "name": name, "description": description}
            data.append(new_profile)
            self.write_to_xlsx_profiles(data)
            if code and name and description:
                values = (code, name, description)
                self.tree.insert('', 'end', values=values)
                self.name_entry.delete(0, 'end')
                self.description_entry.delete(0, 'end')
                if name == self.name_placeholder:
                    self.name_entry.insert(0, self.name_placeholder)
                    self.name_entry.configure(fg='#ABB2B9')
                if description == self.description_placeholder:
                    self.description_entry.insert(0, self.description_placeholder)
                    self.description_entry.configure(fg='#ABB2B9')

    def remove_profile(self):
        selected_item = self.tree.selection()

        if selected_item:
            code = self.tree.item(selected_item, 'values')[0]
            name = self.tree.item(selected_item, 'values')[1]
            description = str(self.tree.item(selected_item, 'values')[2])
            
            data = self.read_from_xlsx_profiles()
            
            for profile in data:
                if profile['code'] == code and profile['name'] == name and profile['description'] == description:
                    data.remove(profile)
                   
                    self.write_to_xlsx_profiles(data)
                    self.tree.delete(selected_item)
        else:
            tkMessageBox.showerror('NOT FOUND', 'Esse cadastro não foi\nencontrado no arquivo.')

    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_profiles({})

        data = self.read_from_xlsx_profiles()
        for profile in data:
            code = profile['code']
            name = profile['name']
            description = profile['description']
            self.tree.insert('', 'end', values=(code, name, description))

    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel('systems.xlsx', engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def write_to_xlsx_profiles(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_profiles(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data                
        except pd.errors.EmptyDataError:
            return {}


class MatrizPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'matriz.xlsx'
        self.filename_systems = 'systems.xlsx'
        self.filename_profiles = 'profiles.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.bg_color = '#17202A'

        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(expand=True, fill='both')

        self.title = tk.Label(frame, text='Registro de Restrições', font=('Roboto', 16), foreground='#48C9B0', background=self.bg_color)
        self.title.pack(padx=20, pady=20)
        self.columns = ('Perfil de Acesso 1', 'Perfil de Acesso 2')
        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=180)

        self.tree.pack(pady=20, expand=True)

        profile_1 = self.create_association_list()
        profile_2 = self.create_association_list()

        self.profile_access_1 = tk.StringVar(self)
        self.profile_access_1.set(profile_1[0])
        profile_access_1_dropdown = ttk.Combobox(frame, textvariable=self.profile_access_1, values=profile_1, foreground='black', font=('Roboto', 14), width=20, justify='center')
        profile_access_1_dropdown.pack(pady=10)

        self.profile_access_2 = tk.StringVar(self)
        self.profile_access_2.set(profile_2[0])
        profile_access_2_dropdown = ttk.Combobox(frame, textvariable=self.profile_access_2, values=profile_2, foreground='black', font=('Roboto', 14), width=20, justify='center')
        profile_access_2_dropdown.pack(pady=10)

        add_button = tk.Button(frame, text='Adicionar à Matriz', command=self.add_to_matrix, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        remove_button = tk.Button(frame, text='Remover', command=self.remove_matrix, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)

        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()

    def add_to_matrix(self):
        
        profile_1 = self.profile_access_1.get()
        profile_2 = self.profile_access_2.get()
        if profile_1 == profile_2:
            tkMessageBox.showerror('INVALID REQUEST', 'Escolha perfis de\nacesso diferentes.')
        else:
            data = self.read_from_xlsx_matriz()
            for item in data:
                item1 = item['profile_access_1']
                item2 = item['profile_access_2']
                if profile_1 == item1 and profile_2 == item2:
                    tkMessageBox.showerror('INVALID', 'Os perfis de acesso\njá foram traçados.')
                    return
            else:
                new_matrix = { "profile_access_1": profile_1, "profile_access_2": profile_2 }
                data.append(new_matrix)
                self.write_to_xlsx_matriz(data)
                self.tree.insert('', 'end', values=(profile_1, profile_2))

    def remove_matrix(self):
        selected_item = self.tree.selection()

        if selected_item:
            profile1 = self.tree.item(selected_item, 'values')[0]
            profile2 = self.tree.item(selected_item, 'values')[1]
            data = self.read_from_xlsx_matriz()

            for profiles in data:
                if profiles['profile_access_1'] == profile1 and profiles['profile_access_2'] == profile2:
                    data.remove(profiles)

                    self.write_to_xlsx_matriz(data)
                    self.tree.delete(selected_item)
        else:
            tkMessageBox.showerror('NOT FOUND', 'Esse registro não\nfoi encontrado.')
    
    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_matriz({})

        data = self.read_from_xlsx_matriz()

        for item in data:

            profile1 = item['profile_access_1']
            profile2 = item['profile_access_2']
            self.tree.insert('', 'end', values=(profile1, profile2))

    def create_association_list(self):
        systems_data = self.read_from_xlsx_systems()
        profiles_data = self.read_from_xlsx_profiles()

        association_list = []

        for profile in profiles_data:
            profile_name = profile['name']

            for _, name in systems_data.items():
                data = f'{profile_name} - {name}'
                association_list.append(data)

        return association_list
    
    def read_from_xlsx_matriz(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data
        except pd.errors.EmptyDataError:
            return {}

    def write_to_xlsx_matriz(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel(self.filename_systems, engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def read_from_xlsx_profiles(self):
        try:
            df = pd.read_excel(self.filename_profiles, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data                
        except pd.errors.EmptyDataError:
            return {}


class UsuariosPage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.filename = 'users.xlsx'
        self.filename_systems = 'systems.xlsx'
        self.filename_profiles = 'profiles.xlsx'
        self.create_widgets()

    def create_widgets(self):
        self.bg_color = '#17202A'

        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(expand=True, fill='both')

        self.title = tk.Label(frame, text='Cadastro de Perfis dos Usuários', font=('Roboto', 16), foreground='#48C9B0', background=self.bg_color)
        self.title.pack(padx=20, pady=20)
        
        self.columns = ('CPF', 'Código do Sistema', 'Nome do Perfil')
        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings', height=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=180)

        self.tree.pack(pady=20, expand=True)

        self.cpf_var = tk.StringVar()

        self.cpf_entry = tk.Entry(frame, width=30, borderwidth=0, highlightthickness=0, bg='#273746', font=('Calibri', 12), justify='center')
        self.cpf_placeholder = 'Insira o CPF do Usuário'
        Focus.setup_entry(self.cpf_entry, self.cpf_placeholder)
        self.cpf_entry.pack(pady=10)

        self.system = self.create_system_list()
        self.profile = self.create_profile_list()

        self.system_entry = tk.StringVar(self)
        self.system_entry.set(self.system[0])
        system_entry_dropdown = ttk.Combobox(frame, textvariable=self.system_entry, values=self.system, foreground='black', font=('Roboto', 14), width=15, justify='center')
        system_entry_dropdown.pack(pady=10)

        self.profile_entry = tk.StringVar(self)
        self.profile_entry.set(self.profile[0])
        profile_entry_dropdown = ttk.Combobox(frame, textvariable=self.profile_entry, values=self.profile, foreground='black', font=('Roboto', 14), width=15, justify='center')
        profile_entry_dropdown.pack(pady=10)

        add_button = tk.Button(frame, text='Adicionar', command=self.add_user, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)
        remove_button = tk.Button(frame, text='Remover', command=self.remove_user, foreground='#48C9B0', bg='#273746', activebackground='#2C3E50', activeforeground='white', font=('Roboto', 14), borderwidth=0, highlightthickness=0, width=15)

        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.load_data()
    

    def add_user(self):
        cpf = self.cpf_entry.get()
        system = self.system_entry.get()
        profile = self.profile_entry.get()
        if not cpf.isdigit() or cpf == '' or len(cpf)>11:
            tkMessageBox.showerror('INVALID DATA', 'Digite um número\nválido para CPF.')
        else:
            data = self.read_from_xlsx_users()
            formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            for item in data:
                cpf_user = item['cpf']
                if formatted_cpf == cpf_user:
                    tkMessageBox.showerror('FORBIDDEN', 'Esse CPF já\nfoi cadastrado.')
                    return
            else:
                new_user = { 'cpf': formatted_cpf, 'system': system, 'profile': profile }
                data.append(new_user)
                self.write_to_xlsx_users(data)
                self.tree.insert('', 'end', values=(formatted_cpf, system, profile))
                self.cpf_entry.delete(0, 'end')
                if self.cpf_entry == self.cpf_placeholder:
                    self.cpf_entry.insert(0, self.cpf_placeholder)
                    self.cpf_entry.configure(fg='#ABB2B9')

    def remove_user(self):
        selected_item = self.tree.selection()

        if selected_item:
            cpf = self.tree.item(selected_item, 'values')[0]
            system = self.tree.item(selected_item, 'values')[1]
            profile = self.tree.item(selected_item, 'values')[2]
            data = self.read_from_xlsx_users()
     
            for item in data:
                if item['cpf'] == cpf and item['system'] == system and item['profile'] == profile:
                    data.remove(item)
                    self.write_to_xlsx_users(data)
                    self.tree.delete(selected_item)
        else:
            tkMessageBox.showerror('NOT FOUND', 'Esse usuário não\nfoi encontrado.')
    
    def load_data(self):
        if not os.path.exists(self.filename):
            self.write_to_xlsx_users({})

        data = self.read_from_xlsx_users()

        for item in data:
            cpf = item['cpf']
            system = item['system']
            profile = item['profile']
            self.tree.insert('', 'end', values=(cpf, system, profile))

    def create_system_list(self):
        systems_data = self.read_from_xlsx_systems()

        system_list = []
        for _, name in systems_data.items():
            system_list.append(name)
        
        return system_list
    
    def create_profile_list(self):
        profiles_data = self.read_from_xlsx_profiles()

        profiles_list = []
        for profile in profiles_data:
            name = profile['name']
            profiles_list.append(name)

        return profiles_list
    
    def read_from_xlsx_users(self):
        try:
            df = pd.read_excel(self.filename, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data
        except pd.errors.EmptyDataError:
            return {}

    def write_to_xlsx_users(self, data):
        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def read_from_xlsx_systems(self):
        try:
            df = pd.read_excel(self.filename_systems, engine='openpyxl')
            data = {row['Código do Sistema']: (row['Nome do Sistema']) for _, row in df.iterrows()}
            return data
        except pd.errors.EmptyDataError:
            return {}
            
    def read_from_xlsx_profiles(self):
        try:
            df = pd.read_excel(self.filename_profiles, engine='openpyxl')
            data = df.to_dict(orient='records')
            return data                
        except pd.errors.EmptyDataError:
            return {}


class AlunosPage(tk.Frame):
    def __init__(self):
        super().__init__()
        # Lista de alunos
        self.alunos = [
            "Roberta Coutinho Paes - Matrícula 202307274356",
            "Rubia Rafaela Nascimento Hilario - Matrícula 202003423769",
            "Ramon Santos Cerqueira - Matrícula 202303875487",
            "Roger Souza Funaki - Matrícula 202301156092",
            "Sara Suely Cavalcante de Souza - Matrícula 20230717735",
            "Thiago Rodrigo Balão - Matrícula 202308210793"
        ]
        self.title = ('Alunos - Grupo 19')
        self.color = '#17202A'

        title_label = tk.Label(self, text=self.title, font=('Roboto', 17), foreground='#48C9B0', bg=self.color)
        title_label.pack(padx=20, pady=20)

        self.configure(bg=self.color)
        for line in self.alunos:
            label = tk.Label(self, text=line, font=('Roboto', 13), foreground='white', bg=self.color)
            label.pack(padx=20, pady=5)



if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
