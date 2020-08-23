from accounts import login, create_account
import os.path

if __name__ == "__main__":
    while True:
        action = input("1 - Autenticarse \n2 - Registrar Usuario \nEnter - Salir\n-> ")
        
        if action == "1":
            login()

        elif action == "2":
            create_account()

        else:
            break