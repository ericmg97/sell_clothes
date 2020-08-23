from utils import *
import os.path

if __name__ == "__main__":
    while True:
        action = input(
            "1 - Autenticarse \n2 - Registrar Usuario \nEnter - Salir\n-> ")
        if action == "1":
            while True:
                name = input("\nEscribe tu nombre: ")

                with open("./users.db") as us:
                    users = json.load(us)

                    if name == "":
                        print()
                        break

                    elif name in users:
                        option = input(
                            "\n1 - Acceder a venta existente\n2 - Crear nueva venta\n-> ")

                        if option == "1":
                            while True:
                                venta = input("\nNombre de venta: ")
                                if venta == "":
                                    print()
                                    break
                                elif venta in users[name]:
                                    temp(name, venta)
                                else:
                                    print("Nombre de venta inexistente \n")

                        elif option == "2":
                            create_sales(name)
                            break
                        else:
                            print()
                            break
                    else:
                        print("Usuario inexistente\n")

        elif action == "2":
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

        else:
            break