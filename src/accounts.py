from utils import create_path
from sales import sales
import json

def create_account():
    name = input("\nEscribe tu nombre: ")

    if name == "":
        print("Cancelado\n")
    else:
        with open("./users.db") as us:
            users = json.load(us)
            if name in users:
                print(
                    "Su nombre ya esta registrado, intente con uno diferente.\n")
            else:
                create_sales(name)
                print("Cuenta creada exitosamente.\n")

def login():
    while True:
        name = input("\nEscribe tu nombre: ")

        with open("./users.db") as us:
            users = json.load(us)

            if name == "":
                print()
                break

            elif name in users:
                while True:
                    option = input(
                        "\n1 - Acceder a venta existente\n2 - Crear nueva venta\n-> ")

                    if option == "1":
                        login_sales(users, name)

                    elif option == "2":
                        create_sales(name)

                    else:
                        print()
                        break
            else:
                print("Usuario inexistente\n")

def create_sales(name):
    with open("./users.db") as us:
        users = json.load(us)

        while True:
            venta = input("\nNombre su venta: ")
            if venta == "":
                print("Nombre no valido, intente con uno diferente")
                continue
            elif name not in users:
                users[name] = {venta: 1}
            elif venta in users[name]:
                print("Nombre existente, intente con uno diferente")
                continue
            else:
                users[name][venta] = 1

            path = create_path(name,venta)

            with open(f"{path}.db", "w") as db:
                json.dump({}, db)

            with open(f"{path}.log", "w") as log:
                pass

            with open(f"{path}_names.db", "w") as names:
                json.dump({}, names)

            with open("./users.db", "w") as user:
                json.dump(users, user)
                        
            print("Venta creada exitosamente. \n")
            break

def login_sales(users, name):
    while True:
        venta = input("\nNombre de venta: ")
        if venta == "":
            print()
            break
        elif venta in users[name]:
            actual_sales = sales(name, venta)

            actual_sales()
        else:
            print("Nombre de venta inexistente \n")