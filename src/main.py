from utils import *
import os.path

def temp(name, venta):
    while True:
        selected = input("1 - Añadir Articulos \n2 - Vender Articulos \n3 - Resumen\n4 - Registro de Ventas\n5 - Buscar Articulos\n6 - Inventario\n7 - Resumen de Ventas Personales\nEnter - Cerrar Sesion\n-> ")
        print()

        if selected == "1":
            add_article(create_path(name,venta))
           
        elif selected == "2":
            sell_article(create_path(name,venta))

        elif selected == '3':
            resume(create_path(name,venta))
        
        elif selected == '4':
            print_log(create_path(name,venta))
            print()
            
        elif selected == '5':
            search = input("Prendas a Localizar: ")
            search = search.split()

            for clothe in search:
                print(search_article(create_path(name,venta), clothe)[2])
            
            print()
        
        elif selected == '6':          
            
            select = input("1 - Añadir prenda\n2 - Revisar faltantes\n3 - Resumen por nombres\n->")
            print()
            if select == '1':
                while True:
                    search = input("Prendas: ")

                    if search == '':
                        break

                    search = search.split()

                    with open("./database.db") as db:
                        data = json.load(db)

                        with open("./inventary.db") as inv: 
                            inven = json.load(inv)

                            for clothe in search:
                                if clothe not in data.keys():
                                    print(f"{clothe}: -> No existe")
                                elif inven[clothe]:
                                    print(f"{clothe}: -> Ya esta en inventario")
                                else:
                                    inven[clothe] = True
                                    info = data[clothe][4]
                                    price = float(data[clothe][0])

                                    print(f'{clothe}: -> Añadido {info} - {data[clothe][3]} -> {price}')
                            print()

                        with open("./inventary.db", "w") as i:
                            json.dump(inven, i)    
            elif select == '2':
                with open("./inventary.db") as inv: 
                    inven = json.load(inv)
                    with open("./database.db") as db:
                        data = json.load(db)
                        lost = []
                        filter = input("Nombre: ")
                        if filter == "todos": 
                            for i in inven.items():
                                if not i[1]:
                                    lost.append(i[0])
                        else:
                            try:
                                for i in inven.items():
                                    if not i[1] and data[i[0]][3] == filter:
                                        lost.append(i[0])
                            except:
                                pass
                        
                        if not len(lost):
                            print("Todo en orden")

                        [print(f'{clothe}: -> {data[clothe][4]} - {data[clothe][3]} -> {float(data[clothe][0])} Vendido->{data[clothe][2]}') for clothe in lost]        

                        print()
            elif select == '3':
                with open("./inventary.db") as inv: 
                    inven = json.load(inv)
                    with open("./database.db") as db:
                        data = json.load(db)
                        with open("./names.db") as nm:
                            names = json.load(nm)
                            rep_name = {}
                            rep_inv = {}
                            for i, name in enumerate(names.items()):
                                rep_inv[name[0]] = 0
                                rep_name[name[0]] = 0
                                for cl in data.items():
                                    if name[0] == cl[1][3]:
                                        rep_name[name[0]] += 1

                                for cl in inven.items():
                                    if name[0] == data[cl[0]][3] and cl[1]:
                                        rep_inv[name[0]] += 1

                            print("\n%-19s%-8s%-10s%-12s%-10s" % ("Nombres", "Total", "Vendido", "Inventario", "Perdido"))
                            print("_"*62)
                            
                            for name in rep_name.items():
                                total = name[1] 
                                vendido = names[name[0]][0]
                                inventario = rep_inv[name[0]]
                                perdido = total - vendido - inventario

                                print("%-20s%-10s%-10s%-12s%-10s" % (name[0], total, vendido, inventario, perdido))

                            print("_"*62)
                            print()

                print()
        elif selected == '7':
            inp = input("Nombre: ")
            with open('./database.db') as db:
                data = json.load(db)
                total = 0
                for cl in data.items():
                    if cl[1][2] and cl[1][3] == inp:
                        print(f"{cl[0]}: {cl[1][4]} -> {cl[1][1]}")
                        total += cl[1][1]
                
                print(f"\nTotal: {total} \n")
        else:
            break


if __name__ == "__main__":
    while True:
        action = input("1 - Autenticarse \n2 - Registrar Usuario \nEnter - Salir\n-> ")
        if action == "1":
            while True:
                name = input("Escribe tu nombre: ")

    	        with open("./users.db") as us:
                    users = json.load(us)

                    if name == "":
                        print()
                        break

                    elif name in users:
                            option = input("1 - Acceder a venta existente\n2 - Crear nueva venta\n-> ")

                            if option == "1": 
                                while True: 
                                    venta = input("\nNombre: ")
                                    if venta == "":
                                        print()
                                        break
                                    elif venta in users[name]:
                                        temp(name, venta)
                                    else:
                                        print("Nombre de venta inexistente \n")
                                        
                            elif option == "2":
                                create_sales(name)
                            else:
                                print()
                                break
                    else:
                        print("Usuario inexistente\n")

        elif action == "2":
            name = input("Escribe tu nombre: ")
            
            if name == "":
                print("Cancelado\n")
            else:
                with open("./users.db") as us:
                    users = json.load(us)
                    if name in users:
                        print("Su nombre ya esta registrado, intente con uno diferente.")
                    else:
                        create_sales(name)

        else:
            pass
                    

def create_sales(name):
    with open("./users.db") as us:
        users = json.load(us)

        while True:
            venta = input("\nNombre su venta: ")
            if venta == "":
                print("Nombre no valido, intente con uno diferente")
                continue
            elif venta in users:
                print("Nombre existente, intente con uno diferente")
                continue
            else:
                users[name] = [venta]

            with open(f"./{name}_1.db", "w") as db:
                json.dump({},db)
            
            with open(f"./{name}_1.log", "w") as log:
                json.dump({},log)

            with open(f"./{name}_1_names.db", "w") as names:
                json.dump({},names)
            
            with open("./users.db", "w") as user:
                json.dump(users,user)

            break