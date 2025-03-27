import json
import hashlib

# Funzione per generare un hash sicuro della password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funzione per caricare i dati degli utenti dal file JSON
def load_users():
    try:
        with open('56data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Funzione per salvare i dati degli utenti nel file JSON
def save_users(users):
    with open('56data.json', 'w') as file:
        json.dump(users, file, indent=4)

# Funzione per registrare un nuovo utente
def register():
    users = load_users()
    username = input("Inserisci il nome utente: ")
    
    if username in users:
        print("Nome utente già esistente. Scegli un altro nome utente.")
        return

    password = input("Inserisci la password: ")
    hashed_password = hash_password(password)
    
    # Aggiungi il nuovo utente al dizionario
    users[username] = hashed_password
    save_users(users)
    print("\nRegistrazione avvenuta con successo!")

# Funzione per autenticare un utente
def login():
    users = load_users()
    username = input("Inserisci il nome utente: ")

    if username not in users:
        print("Nome utente non trovato.")
        return

    password = input("Inserisci la password: ")
    hashed_password = hash_password(password)
    
    if users[username] == hashed_password:
        print("\nBenvenuto! ")
        print(username)
    else:
        print("\nPassword errata.")

# Funzione principale
def main():
    while True:
        print("\nSeleziona un'opzione:")
        print("1. Registrazione")
        print("2. Login")
        print("3. Esci")
        choice = input("Scelta: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Uscita...")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()