from cryptography.fernet import Fernet
from getpass import getpass
import os

MASTER_PASSWORD = "harsh2004"  # Change this!

'''
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)'''

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

def verify_master_password():
    attempt = getpass("Enter master password: ")
    return attempt == MASTER_PASSWORD

key = load_key()
fer = Fernet(key)

def view():
    if not verify_master_password():
        print("✖ Incorrect master password. Access denied.")
        return
    
    try:
        with open('passwords.txt', 'r') as f:
            print("\nStored Passwords:")
            print("-----------------")
            for line in f.readlines():
                data = line.rstrip()
                if data:  # Skip empty lines
                    parts = data.split("|", 2)
                    if len(parts) == 3:
                        user, passw, note = parts
                        print(f"User: {user} | Password: {fer.decrypt(passw.encode()).decode()} | Note: {note}")
                    else:
                        user, passw = parts
                        print(f"User: {user} | Password: {fer.decrypt(passw.encode()).decode()} | Note: (none)")
            print("-----------------\n")
    except FileNotFoundError:
        print("ℹ No passwords stored yet.")


def add():
    if not verify_master_password():
        print("✖ Incorrect master password. Access denied.")
        return
    
    name = input('Account Name: ')
    pwd = getpass("Password: ")
    note = input("Note/Description: ")

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "|" + note + "\n")
    print("✔ Password added successfully.")


def delete():
    if not verify_master_password():
        print("✖ Incorrect master password. Access denied.")
        return
    
    account_to_delete = input("Enter account name to delete: ")
    temp_file = "passwords.tmp"
    deleted = False
    
    try:
        with open('passwords.txt', 'r') as f:
            with open(temp_file, 'w') as temp:
                for line in f.readlines():
                    data = line.rstrip()
                    if data:
                        parts = data.split("|", 2)
                        user = parts[0]
                        if user != account_to_delete:
                            temp.write(line)
                        else:
                            deleted = True
        
        if deleted:
            os.remove('passwords.txt')
            os.rename(temp_file, 'passwords.txt')
            print(f"✔ Account '{account_to_delete}' deleted successfully.")
        else:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"✖ Account '{account_to_delete}' not found.")
                
    except FileNotFoundError:
        print("ℹ No passwords stored yet.")
    except Exception as e:
        print(f"✖ An error occurred: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)


while True:
    print("\nOptions:")
    print("1. View passwords (view)")
    print("2. Add new password (add)")
    print("3. Delete password (delete)")
    print("4. Quit (q)")
    
    mode = input("\nChoose an option (view/add/delete/q): ").lower().strip()
    
    if mode == "q":
        print("Goodbye!")
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    elif mode == "delete":
        delete()
    else:
        print("⚠ Invalid option. Please choose view, add, delete, or q.")