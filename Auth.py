import bcrypt
import pandas as pd
import tkinter.messagebox as tkMessageBox

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def authenticateUser(user, password):
    user_lower = user.lower()
    users_profiles = read_from_xlsx('passwords.xlsx')

    if user_lower in users_profiles:
        stored_hash = users_profiles[user_lower]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True
        else:
            tkMessageBox.showerror('UNAUTHORIZED', 'Usuário ou senha incorretos')
    else:
        return False
    
    return False

def write_to_xlsx(filename, data):
    data_str = {user: hash_.decode('utf-8') for user, hash_ in data.items()}
    df = pd.DataFrame(list(data_str.items()), columns=['Username', 'Hashed_Password'])
    df.to_excel(filename, index=False)

def read_from_xlsx(filename):
    df = pd.read_excel(filename)
    data = {row['Username'].lower(): row['Hashed_Password'].encode('utf-8') for _, row in df.iterrows()}
  
    return data


hashed_passwords = {
    'admin': hash_password('#00#Estacio23'),
    'aluno':  hash_password('#01#Estacio23'),
}


write_to_xlsx('passwords.xlsx', hashed_passwords)
users_options = read_from_xlsx('passwords.xlsx')
