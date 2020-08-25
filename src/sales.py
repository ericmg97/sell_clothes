import json
from utils import *

class sales:
    def __init__(self, name, sale):
        self.name = name
        self.sale = sale
        self.path = create_path(name, sale)

    def __call__(self):
        while True:
            selected = input("\n1 - Articulos\n2 - Inventario \n3 - Resumen\nEnter - Salir\n-> ")
            print()
            

            if selected == "1":
                while(True):
                    opt = input("1 - Añadir \n2 - Vender \n3 - Cambiar Precios \n4 - Devolucion \n5 - Buscar \n6 - Cerrar Corte\nEnter - Atras\n-> ")
                    print()
                    
                    if opt == "1":
                        self.add_article()
                    
                    elif opt == "2":
                        self.sell_article()

                    elif opt == '3':
                        self.change_prices()  

                    elif opt == '4':
                        self.return_article()

                    elif opt == '5':
                        self.advanced_search()
                    
                    elif opt == '6':
                        self.make_cut()

                    else:
                        break

            elif selected == '2':
                self.inventory()

            elif selected == "3":
                sel = input("1 - Ventas \n2 - Nombres \n3 - Estado\nEnter - Atras\n-> ")
                print()
                
                if sel == "1":
                    self.resume()
                
                elif sel == "2":
                    select = input("Nombre: ")          
                    self.resume_names(select)

                elif sel == "3":
                    with open(f"{self.path}.db") as db:
                        data = json.load(db)

                        with open(f"{self.path}_names.db") as nm:
                            names = json.load(nm)

                            rep_name = {}
                            rep_inv = {}
                            rep_returned = {}
                            for i, name in enumerate(names.items()):
                                
                                rep_inv[name[0]] = 0
                                rep_returned[name[0]] = 0
                                rep_name[name[0]] = 0

                                for cl in data.items():
                                    if name[0] == cl[1][3]:
                                        rep_name[name[0]] += 1
                                        if not cl[1][2] and cl[1][5] and cl[1][6]:
                                            rep_inv[name[0]] += 1
                                        elif not cl[1][5] and not cl[1][2]:
                                            rep_returned[name[0]] += 1
                                        
                            print("\n%-19s%-8s%-10s%-12s%-10s%10s" % ("Nombres",
                                                                "Total", "Vendido", "Inventario", "Entregado", "Faltantes"))
                            print("_"*70)

                        for name in rep_name.items():
                            total = name[1]
                            vendido = 0
                            for cut in names[name[0]][0]:
                                vendido += cut

                            inventario = rep_inv[name[0]]
                            entregado = rep_returned[name[0]]

                            print("%-20s%-10s%-10s%-12s%-10s%-10s" %
                                (name[0], total, vendido, inventario, entregado, total - vendido - inventario - entregado))

                        print("_"*70)
                        print()

            else:
                break
  
    def add_article(self):
        with open(f"{self.path}.db") as r:
            data = json.load(r)
            
            try:
                curr_art = int(list(data.keys())[-1]) + 1
            except:
                curr_art = 1

            while True:
                name = input("Dueño del articulo: ")
                if name == "":
                    print()
                    return

                with open(f"{self.path}_names.db") as nm:
                    names = json.load(nm)

                    if name not in names:
                        self.add_name(name)
                    else:
                        print()

                    while True:
                        info = input(
                            f"Añadir informacion de articulo {curr_art}: ")

                        if not len(info):
                            print()
                            break

                        prices = input(
                            f"Añadir precios de articulo {curr_art} (Venta Costo): ").split()

                        sure = input("Confirmar: ")
                        if sure != "":
                            print("Cancelado\n")
                            continue

                        try:
                            if len(prices) == 2:
                                data[curr_art] = (float(prices[0]), float(
                                    prices[1]), False, name, info, True, False)
                            else:
                                data[curr_art] = (float(prices[0]), float(
                                    prices[0]), False, name, info, True, False)

                            print(f"Articulo Añadido Exitosamente \n")

                            with open(f"{self.path}.db", "w") as db:
                                json.dump(data, db)

                            curr_art += 1
                        except:
                            print("Los datos introducidos son incorrectos. Cancelado\n")
                            pass

    def change_prices(self):
        while True:
            art = input("Numero de serie: ")
            print()
            
            if art == "":
                print()
                break

            cl = self.search_article(art)

            with open(f"{self.path}.db") as r:
                data = json.load(r)

                if cl[0]:
                    print(f"{cl[2]} {data[art][1]}")
                    prices = input("Nuevos Precios (Venta Costo): ").split()
                    
                    try:
                        if len(prices) == 2:
                            data[art][0] = float(prices[0])
                            data[art][1] = float(prices[1])
                        else:
                            data[art][0] = float(prices[0])
                            data[art][1] = float(prices[0])

                        print(f"Precios cambiados exitosamente \n")

                        with open(f"{self.path}.db", "w") as db:
                            json.dump(data, db)

                    except:
                        print("Los datos introducidos son incorrectos. Cancelado\n")
                        pass
                else:
                    print(cl[2])
                    print("No se pueden modificar sus precios\n")

    def add_name(self, name):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)

            while True:
                gain = input("Porciento de ganancia (0-100): ")
                try:
                    if gain == "":
                        gain = 0
                    elif int(gain) < 0 or int(gain) > 100:
                        print("Porciento incorrecto")
                        continue

                    names[name] = ([0], [0], [0], int(gain), [[]])
                    with open(f"{self.path}_names.db", "w") as nm:
                        json.dump(names, nm)

                    print()
                    break
                except:
                    print("Porciento incorrecto -> (0-100)")

    def sell_article(self):
        while True:
            clothes = input("Prendas a vender:")
            clothes = clothes.split()

            if not len(clothes):
                print()
                return

            tot_price = 0
            sold = clothes[:]

            for clothe in clothes:
                art = self.search_article(clothe)

                if art[0]:
                    price = float(art[1][0])
                    tot_price += price

                print(art[2])

            print(f"\nPrecio Total: {tot_price}\n")

            sure = input("Confirmar: ")

            if(sure == ""):
                print("OK\n")

                with open(f"{self.path}.db") as db:
                    data = json.load(db)

                    with open(f"{self.path}_names.db",) as nm:
                        names = json.load(nm)

                        for clothe in sold:
                            temp = data[clothe]

                            names[temp[3]][0][-1] += 1
                            names[temp[3]][1][-1] += float(temp[0])
                            names[temp[3]][2][-1] += float(temp[1]) - float(temp[1])*names[temp[3]][3]/100
                            names[temp[3]][4][-1].append(clothe)

                            data[clothe] = (temp[0], temp[1],
                                            True, temp[3], temp[4], temp[5], True)

                        if len(sold):
                            log(f"{self.path}.log", "-> Prendas vendidas:", *clothes)

                        with open(f"{self.path}.db", "w") as dw:
                            json.dump(data, dw)

                        with open(f"{self.path}_names.db", "w") as nm:
                            json.dump(names, nm)
            else:
                print("Cancelado\n")

    def return_article(self): #terminar
        pass

    def resume(self):
        while(True):
            sel = input("Cortes a resumir: \n1 - Todos\n2 - Ultimo\n3 - Seleccion Manual\n-> ")

            if sel == "":
                print()
                return
            elif sel == "1":
                with open("./users.db") as us:
                    users = json.load(us)

                    cuts = [i for i in range(0, users[self.name][self.sale])]
                    self.__resume__(cuts)

            elif sel == "2":
                with open("./users.db") as us:
                    users = json.load(us)

                    cuts = [users[self.name][self.sale] - 1]
                    self.__resume__(cuts)

            elif sel == "3":
                cut = input("\nCortes: ")
                try:
                    cuts = {int(x) - 1 for x in cut.split()}             
                    self.__resume__(cuts)
                except:
                    print("Entrada Invalida\n")
                    continue

    def __resume__(self, cuts):
        with open(f"{self.path}.db") as db:
            with open(f"{self.path}_names.db") as nm:
                names = json.load(nm)
                data = json.load(db)
                    
                total = 0
                cant = 0
                total_gan = 0
                total_dar = 0
                sold_out = []

                if not self.check_cuts(cuts):
                    return

                print("\n%-17s%-13s%-10s%-10s%-10s%-10s" % ("Nombres", "Cantidad",
                                                            "Total", "Entregar", "Ganancia", "Prendas Vendidas"))
                print("_"*80)

                for name in names.items():
                    total_name = [0,0,0,0,[]]
                    
                    for cut in cuts:
                        cant += name[1][0][cut]
                        total += name[1][1][cut]
                        total_gan += name[1][1][cut] - name[1][2][cut]
                        total_dar += name[1][2][cut]
                        sold_out.extend(name[1][4][cut])

                        total_name[0] += name[1][0][cut]
                        total_name[1] += name[1][1][cut]
                        total_name[2] += name[1][2][cut]
                        total_name[4].extend(name[1][4][cut])

                    print("%-20s%-10s%-10s%-10s%-10s" %
                        (name[0], total_name[0], total_name[1], total_name[2], total_name[1] - total_name[2]), *total_name[4])

                print("_"*80)
                print("%-20s%-10s%-10s%-10s%-10s" %
                    ("General", cant, total, total_dar, total_gan), *sold_out)
                print()

    def add_to_inventory(self):
        while True:
            ad = input("Añadir prenda: ")
            if ad == "":
                print()
                break
            else:
                list_art = ad.split()
                ad_art = []
                for art in list_art:
                    search = self.search_article(art)
                    if search[0]:
                        ad_art.append(art)
                        
                    print(search[2])
                
                sure = input("Seguro: ")
                if sure == "":
                    with open(f"{self.path}.db") as db:
                        data = json.load(db)

                        for cl in ad_art:
                            data[cl][6] = True

                        with open(f"{self.path}.db", "w") as d:
                            json.dump(data, d)

                    print("Prendas añadidas correctamente. \ns")
                else:
                    print("Cancelado.\n")
                    continue

    def check_lost(self, name):
        with open(f"{self.path}.db") as db:
            data = json.load(db)
            
            lost = []
            
            if name == "todos":
                for cl in data.items():
                    if cl[1][5] and not cl[1][6]:
                        lost.append(cl[0])
            else:
                try:
                    for cl in data.items():
                        if cl[1][5] and not cl[1][6] and cl[1][3] == name:
                            lost.append(cl[0])
                except:
                    pass

            [print(f'{clothe}: {data[clothe][3]} - {data[clothe][4]} -> {float(data[clothe][0])}')
                for clothe in lost]

            print(f"\nTotal: {len(lost)}")

            print()  

    def check_inventory(self, name):
            with open(f"{self.path}.db") as db:
                data = json.load(db)
            
            inven = []
                      
            try:
                for cl in data.items():
                    if cl[1][5] and not cl[1][2] and cl[1][6] and cl[1][3] == name:
                        inven.append(cl[0])
            except:
                pass

            [print(f'{clothe}: {data[clothe][3]} - {data[clothe][4]} -> {float(data[clothe][0])}')
                for clothe in inven]

            print(f"\nTotal: {len(inven)}")

            print()  

    def check_sold(self, name, cuts):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)
            
            total = 0
            cant = 0

            if not self.check_cuts(cuts):
                return

            with open(f"{self.path}.db") as db:
                data = json.load(db)

                for cut in cuts:
                    try:       
                        for cl in names[name][4][cut]:
                            print(f"{cl}: {data[cl][4]} -> {data[cl][1]}")
                            cant += 1
                            total += data[cl][1]
                    except:
                        break

            print(f"\nTotal: {cant} \nValor: {total} \n")

    def check_returned_to_owners(self, name):
        with open(f"{self.path}.db") as db:
            data = json.load(db)
            
            inven = []
                      
            try:
                for cl in data.items():
                    if not cl[1][5] and not cl[1][2] and cl[1][3] == name:
                        inven.append(cl[0])
            except:
                pass

            [print(f'{clothe}: {data[clothe][3]} - {data[clothe][4]} -> {float(data[clothe][0])}')
                for clothe in inven]

            print(f"\nTotal: {len(inven)}")

            print() 

    def check_cuts(self, cuts):
        with open("./users.db") as us:
            users = json.load(us)
            stop = False
            for cut in cuts:
                if cut < 0 or cut >= users[self.name][self.sale]:
                    stop = True
                    print(f"Corte {cut + 1} inexistente") 
            
            if stop:
                print()
                return False
            
            return True

    def return_clothe_to_owner(self):
        owner = input("Nombre: ")
        
        if owner == "":
            print()
            return

        with open(f"{self.path}.db") as db:
            data = json.load(db)
            change = False
            for cl in data:
                if data[cl][3] == owner:
                    change = True
                    data[cl][5] = False

            with open(f"{self.path}.db", "w") as d:
                json.dump(data, d)
        if change:
            print("Ropa entregada correctamente.\n")
        else:
            print("Dueño no encontrado en la lista. \n")

    def delete_inventory(self):
        sure = input("Estas serguro: ")
                
        if sure == "":
            with open(f"{self.path}.db") as db:
                data = json.load(db)

                for cl in data:
                    if data[cl][5] and not data[cl][2]:
                        data[cl][6] = False
                
                with open(f"{self.path}.db", "w") as d:
                    json.dump(data,d)
            
            print("Inventario borrado correctamente. \n")
        else:
            print("Cancelado. \n")

    def inventory(self): 
        while True:
            opt = input("1 - Realizar Inventario\n2 - Revisar faltantes \n3 - Entregar ropa al dueño\n4 - Borrar Inventario\nEnter - Atras\n-> ")
            print()
            
            if opt == "1":
                self.add_to_inventory()
            
            elif opt == "2":        
                name = input("Nombre: ")

                self.check_lost(name)

            elif opt == "3":
                self.return_clothe_to_owner()

            elif opt == "4":
                self.delete_inventory()

            else:
                print()
                return

    def advanced_search(self): 
        while True:
            typ = input("1 - Busqueda por numero de serie\n2 - Busqueda por descripcion\n3 - Busqueda por nombre\nEnter - Atras\n-> ")
            print()

            if typ == "1":
                search = input("Prendas a Localizar: ")
                search = search.split()

                for clothe in search:
                    print(self.search_article(clothe)[2])

                print()
            
            elif typ == "2":
                inp = input("Descripcion: ")
                self.search_description(inp)    
                print()

            elif typ == "3":
                name = input("Nombre: ")

                if name == "":
                    continue

                with open(f"{self.path}_names.db") as nm:
                    names = json.load(nm)
                
                    desc = input("Descripcion: ")
                    print()
                    
                    self.search_description(desc,name)   

                    print()

            else:
                return

    def search_description(self, desc, name = ""):
        if desc == "":
            return
            print()

        with open(f"{self.path}.db") as db:
            data = json.load(db)
            
            for cl in data.items():
                if desc in cl[1][4] and name in cl[1][3]:
                    info = cl[1][4]
                    name = cl[1][3]
                    price = float(cl[1][0])
                    
                    if not cl[1][5]:
                        print(f"{cl[0]}: {name} - {info} -> {price} (Devuelto)")
                    elif cl[1][2]:
                        print(f"{cl[0]}: {name} - {info} -> {price} (Vendido)")
                    elif cl[1][6]:
                        print(f"{cl[0]}: {name} - {info} -> {price} (En inventario)")
                    else:
                        print(f"{cl[0]}: {name} - {info} -> {price}")
                                           
    def search_article(self, art):
        with open(f"{self.path}.db") as db:
            data = json.load(db)

            try:
                info = data[art][4]
                name = data[art][3]
                price = float(data[art][0])

                if not data[art][5]:
                    return (False, data[art][:], f"{art}: {name} - {info} -> {price} (Devuelto)")
                elif data[art][2]:
                    return (False, data[art][:], f"{art}: {name} - {info} -> {price} (Vendido)")
                elif data[art][6]:
                    return (True, data[art][:], f"{art}: {name} - {info} -> {price} (En inventario)")
                else:
                    return (True, data[art][:], f"{art}: {name} - {info} -> {price}")

            except:
                return (False, None, f"{art}: No existe")

    def make_cut(self):
        sure = input("Estas seguro: ")
        if sure == "":
            with open(f"{self.path}_names.db") as nm:
                names = json.load(nm)

                for name in names:
                    names[name][0].append(0)
                    names[name][1].append(0)
                    names[name][2].append(0)
                    names[name][4].append([])

                with open(f"{self.path}_names.db", "w") as n:
                    json.dump(names,n)

                with open("users.db") as u:
                    users = json.load(u)

                    users[self.name][self.sale] += 1

                    with open(f"{self.path}_names.db", "w") as n:
                        json.dump(names,n)

                    print(f"Corte {users[self.name][self.sale] - 1} cerrado")
            
        else:
            print("Cancelado\n")

    def resume_names(self, name):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)
                
            if name not in names:
                print("Ese nombre no existe.\n")
                return
                
            while(True):
                sel = input("\nCortes a resumir: \n1 - Todos\n2 - Ultimo\n3 - Seleccion Manual\nEnter - Atras\n-> ")

                if sel == "":
                    print()
                    return
                elif sel == "1":
                    with open("./users.db") as us:
                        users = json.load(us)
                        cuts = [i for i in range(0, users[self.name][self.sale])]
                        
                        print("\nPrendas Vendidas: ")
                        self.check_sold(name, cuts)        

                        print("\nPrendas En Inventario: ")
                        self.check_inventory(name)

                        print("\nPrendas Devueltas:")
                        self.check_returned_to_owners(name)

                elif sel == "2":
                    with open("./users.db") as us:
                        users = json.load(us)
                        cuts = [users[self.name][self.sale] - 1]

                        print("\nPrendas Vendidas: ")
                        self.check_sold(name, cuts)  

                elif sel == "3":
                    cut = input("\nCortes: ")
                    try:
                        cuts = {int(x) - 1 for x in cut.split()}             
                        
                        print("\nPrendas Vendidas: ")
                        self.check_sold(name, cuts)  
                    except:
                        print("Entrada Invalida\n")
                        continue
