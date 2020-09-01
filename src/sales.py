import json
from utils import *

class sales:
    def __init__(self, name, sale):
        self.name = name
        self.sale = sale
        self.path = create_path(name, sale)

    def __call__(self):
        while True:
            with open("./users.db") as us:
                users = json.load(us)
                print()
                print("_"*18)
                print(f"\n     CORTE {users[self.name][self.sale]}")
                print("_"*18)
                print()


            selected = input("\n1 - Articulos\n2 - Inventario \n3 - Resumen\n4 - Historial\nEnter - Salir\n-> ")
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
                        break

                    else:
                        break

            elif selected == '2':
                self.inventory()

            elif selected == "3":
                while True:
                    sel = input("1 - Ventas \n2 - Nombres \n3 - Estado\nEnter - Atras\n-> ")
                    print()
                    
                    if sel == '':
                        break

                    if sel == "1":
                        cuts = self.select_cuts()
                        print()

                        if len(cuts):
                            while True:
                                inp = input("1 - General\n2 - Personales\nEnter - Atras\n-> ")

                                if inp == "":
                                    print()
                                    break
                                elif inp == "1":
                                    self.resume_sales(cuts)
                                elif inp == "2":
                                    nm = input("\nNombre: ")
                                    if nm == "":
                                        print("Cancelado.\n")
                                    else:
                                        self.info_sold(self.check_sold(nm, cuts))

                            continue                          
                    
                    elif sel == "2":
                        select = input("Nombre: ") 
                        if select == "":
                            print()
                            continue

                        self.resume_names(select)

                    elif sel == "3":
                        self.status()

            elif selected == "4":
                cuts = self.select_cuts()
                print()
                
                self.history(cuts)

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
                                if float(prices[0]) >= float(prices[1]):
                                    data[curr_art] = (float(prices[0]), float(
                                        prices[1]), False, name, info, True, False)
                                else:
                                    print("El precio de venta debe ser mayor o igual al precio de costo\nCancelado\n")
                                    continue
                            elif len(prices) == 1:
                                data[curr_art] = (float(prices[0]), float(
                                    prices[0]), False, name, info, True, False)
                            else:
                                raise ValueError

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

            self.info_articles([art])

            with open(f"{self.path}.db") as r:
                data = json.load(r)

                if cl[0]:
                    prices = input("Nuevos Precios (Venta Costo): ").split()
                    
                    try:
                        if len(prices) == 2:
                            if float(prices[0]) >= float(prices[1]):
                                data[art][0] = float(prices[0])
                                data[art][1] = float(prices[1])
                            else:
                                print("El precio de venta debe ser mayor o igual al precio de costo\nCancelado\n")
                                continue
                        elif len(prices) == 1:
                            data[art][0] = float(prices[0])
                            data[art][1] = float(prices[0])

                        print(f"Precios cambiados exitosamente \n")

                        with open(f"{self.path}.db", "w") as db:
                            json.dump(data, db)

                    except:
                        print("Los datos introducidos son incorrectos. Cancelado\n")
                        pass
                else:
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
                    
                    with open(f"users.db") as us:
                        users = json.load(us)
                        
                        act_cut = users[self.name][self.sale]

                        names[name] = ([0], [0], [0], int(gain), [[]])

                        for cut in range(act_cut - 1):
                            names[name][0].append(0)
                            names[name][1].append(0)
                            names[name][2].append(0)
                            names[name][4].append([])

                        
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

            self.info_articles(clothes)

            for clothe in clothes:
                art = self.search_article(clothe)

                if art[0]:
                    price = float(art[1][0])
                    tot_price += price
                else:
                    sold.remove(clothe)

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
    
    def info_articles(self, arts):
        print("_"*107)
        print("\n%-7s|%-20s|%-45s|%-10s|%-10s|%-10s|" % ("No", "Dueño",
                                                            "Informacion", "Venta", "Costo", "Estado"))
        print("_"*107)

        inv = []
        for art in arts:
            cl = self.search_article(art)

            if cl[1] is not None:
                print("%-7s|%-20s|%-45s|%-10s|%-10s|%-10s|" %
                    (art, cl[1][3], cl[1][4], cl[1][0], cl[1][1], cl[2]))

            else:
                inv.append(cl[2])
        
        print("_"*107)
        print()
        
        for i in inv:
            print(i)

        print()

    def info_sold(self, arts):
        print("_"*75)
        print("\n%-7s|%-45s|%-10s|%-10s|" % ("No", "Informacion", "Costo", "Estado"))
        print("_"*75)

        inv = []
        cant = 0
        money = 0

        for art in arts:
            cl = self.search_article(art)
            cant += 1
            money += cl[1][1]

            if cl[1] is not None:
                print("%-7s|%-45s|%-10s|%-10s|" %
                    (art, cl[1][4], cl[1][1], cl[2]))

            else:
                inv.append(cl[2])
        
        print("_"*75)
        print(f"\nTotal: {cant} -> {money}$")
        print()
        
        for i in inv:
            print(i)

        print()

    def return_article(self):
        serial = input("Numero de serie: ")
        print()

        with open(f"{self.path}.db") as db: 
            data = json.load(db)
            
            if serial == "":
                return

            elif serial not in data:
                print("No existe \n")
                return

            with open(f"{self.path}_names.db") as nm:
                names = json.load(nm)

                for n in names:
                    if serial in names[n][4][-1]:
                        names[n][0][-1] -= 1
                        names[n][1][-1] -= data[serial][0]
                        names[n][2][-1] -= data[serial][1]
                        names[n][4][-1].remove(serial) 

                        data[serial][2] = False
                        data[serial][5] = True
                        data[serial][6] = False

                        with open(f"{self.path}_names.db", "w") as nm:
                            json.dump(names, nm)
                            
                        with open(f"{self.path}.db", "w") as dw:
                            json.dump(data, dw)

                        with open(f"{self.path}.log") as logfile:
                            lines = logfile.readlines()

                            for line in range(len(lines)):
                                if serial in lines[line]:
                                    l_split = lines[line].split()

                                    if l_split[-1] == serial and l_split[-2] == "vendidas:":
                                        lines.pop(line)

                                    else:
                                        for i in range(len(l_split)):
                                            if l_split[i] == serial:
                                                l_split.pop(i)
                                                break
                                        
                                        li = " ".join(l_split)

                                        lines.pop(line)                        
                                        lines.insert(line, f"{li}\n")                  
                                    
                                    with open(f"{self.path}.log", "w") as logfile:
                                        logfile.writelines(lines)

                                    break
                        
                        print("Articulo devuelto exitosamente. \n")
                        break

                else:
                    print("El articulo no ha sido vendido en este corte. \n")

    def select_cuts(self):
        while(True):
            sel = input("Cortes a resumir: \n1 - Todos\n2 - Ultimo\n3 - Seleccion Manual\n-> ")

            cuts = []

            if sel == "":
                return cuts

            elif sel == "1":
                with open("./users.db") as us:
                    users = json.load(us)
                    cuts = [i for i in range(0, users[self.name][self.sale])]
                    break

            elif sel == "2":
                with open("./users.db") as us:
                    users = json.load(us)
                    cuts = [users[self.name][self.sale] - 1]
                    break


            elif sel == "3":
                cut = input("\nCortes: ")
                try:
                    cuts = {int(x) - 1 for x in cut.split()} 
                    
                    if not self.check_cuts(cuts):
                        print("Entrada Invalida\n")
                        continue
                    
                    break            
                except:
                    print("Entrada Invalida\n")
                    continue

        return cuts

    def resume_sales(self, cuts):
        with open(f"{self.path}.db") as db:
            with open(f"{self.path}_names.db") as nm:
                names = json.load(nm)
                data = json.load(db)
                    
                total = 0
                cant = 0
                total_gan = 0
                total_dar = 0
                sold_out = []

                print("_"*64) 
                print("\n%-20s|%-10s|%-10s|%-10s|%-10s|" % ("Nombres", "Cantidad",
                                                            "Total", "Entregar", "Ganancia"))
                print("_"*64)

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
                    
                    if total_name[0]:
                        print("%-20s|%-10s|%-10.2f|%-10.2f|%-10.2f|" %
                            (name[0], total_name[0], total_name[1], total_name[2], total_name[1] - total_name[2]))

                print("_"*64)
                print("%-20s|%-10s|%-10.2f|%-10.2f|%-10.2f|" %
                    ("General", cant, total, total_dar, total_gan))
                    
                print()

    def add_to_inventory(self):
        while True:
            ad = input("Añadir prendas: ")
            if ad == "":
                print()
                break
            else:
                list_art = ad.split()
                ad_art = []

                self.info_articles(list_art)

                for art in list_art:
                    search = self.search_article(art)
                    if search[0] and not search[1][6] and search[1][5]:
                        ad_art.append(art)
                    else:
                        print(f"{art}: Error al añadir")
               
                if not len(ad_art):
                    continue

                sure = input("\nSeguro: ")
                if sure == "":
                    with open(f"{self.path}.db") as db:
                        data = json.load(db)

                        for cl in ad_art:
                            data[cl][6] = True

                        with open(f"{self.path}.db", "w") as d:
                            json.dump(data, d)

                    print("Prendas añadidas correctamente. \n")
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

            return lost

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

            return inven

    def check_sold(self, name, cuts):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)
            
            total = 0
            cant = 0

            if not self.check_cuts(cuts):
                return

            with open(f"{self.path}.db") as db:
                data = json.load(db)
                clothes = []

                for cut in cuts:
                    try:       
                        for cl in names[name][4][cut]:                           
                                clothes.append(cl)
                    except:
                        break
                
            return clothes

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

            return inven

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
        while True:
            owner = input("Nombre: ")
            
            if owner == "":
                print()
                return

            with open(f"{self.path}_names.db") as nm:
                names = json.load(nm)
                    
                if owner not in names:
                    print("Ese nombre no existe.\n")
                    continue

            opt = input("\n1 - Todas \n2 - Seleccion \nEnter - Atras \n-> ") 
            clothes = []
    
            if opt == "1":
                clothes = self.check_inventory(owner)

            elif opt == "2":
                cloth = input("\nPrendas: ")
                cloth = cloth.split()

                for cl in cloth:
                    if self.search_article(cl)[0]:
                        clothes.append(cl)
            
            else:
                print()
                continue

            with open(f"{self.path}.db") as db:
                data = json.load(db)
                
                info = []
                for cl in clothes:            
                    if data[cl][3] == owner:
                        if data[cl][6] and not data[cl][2] and data[cl][5]:
                            info.append(cl)               
                            data[cl][5] = False
                
                print("\nPrendas Entregadas: \n")         
                
                if len(info):
                    self.info_articles(info)

                with open(f"{self.path}.db", "w") as d:
                    json.dump(data, d)

            print()

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
                name = input("1 - Todos\n2 - Por Nombre\nEnter - Atras\n->")
                if name == "1":
                    lost = self.check_lost("todos")
                    self.info_articles(lost)

                    print(f"Total: {len(lost)}\n")

                
                elif name == "2":
                    nm = input("\nNombre: ")
                    lost = self.check_lost(nm)
                    self.info_articles(lost)

                    print(f"Total: {len(lost)}\n")
               
                else:
                    continue
                
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
                
                self.info_articles(search)
                
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
            clothes = []
            for cl in data.items():
                if desc in cl[1][4] and name in cl[1][3]:      
                    clothes.append(cl[0])

            self.info_articles(clothes)

    def search_article(self, art):
        with open(f"{self.path}.db") as db:
            data = json.load(db)

            try:
                info = data[art][4]
                name = data[art][3]
                price = float(data[art][0])

                if data[art][2]:
                    return (False, data[art][:], "Vendido")
                elif not data[art][5]:
                    return (False, data[art][:], "Devuelto")
                elif data[art][6]:
                    return (True, data[art][:], "En inventario")
                else:
                    return (True, data[art][:], "Ok")

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

                    with open(f"users.db", "w") as us:
                        json.dump(users,us)

                    print(f"Corte {users[self.name][self.sale] - 1} cerrado\n")
            
        else:
            print("Cancelado\n")

    def resume_names(self, name):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)
                
            if name not in names:
                print("Ese nombre no existe.\n")
                return
                   
            with open("./users.db") as us:
                users = json.load(us)
                cuts = [i for i in range(0, users[self.name][self.sale])]
                clothes = []

                clothes.extend(self.check_sold(name, cuts))      

                clothes.extend(self.check_inventory(name))

                clothes.extend(self.check_lost(name))

                clothes.extend(self.check_returned_to_owners(name))

                self.info_articles(clothes)

                print(f"Total: {len(clothes)}\n")

    def status(self):
        with open(f"{self.path}_names.db") as nm:
            names = json.load(nm)

            with open("./users.db") as us:
                users = json.load(us)
                cuts = [i for i in range(0, users[self.name][self.sale])]
                
                
                print("_"*77)        
                print("\n%-20s|%-10s|%-10s|%-12s|%-10s|%10s|" % ("Nombres",
                                                    "Total", "Vendido", "Inventario", "Entregado", "Faltantes"))
                print("_"*77)
                tot_v = tot_i = tot_e = tot_f = tot_t = 0
                
                inactive = []

                for name in names.items():
                    vendido = len(self.check_sold(name[0],cuts))
                    tot_v += vendido
                    inventario = len(self.check_inventory(name[0]))
                    tot_i += inventario
                    entregado = len(self.check_returned_to_owners(name[0]))
                    tot_e += entregado
                    faltante = len(self.check_lost(name[0]))
                    tot_f += faltante
                    total = vendido + inventario + entregado + faltante
                    tot_t += total

                    if vendido + entregado != total:
                        print("%-20s|%-10s|%-10s|%-12s|%-10s|%-10s|" %
                            (name[0], total, vendido, inventario, entregado, faltante))
                    else:
                        tot_v -= vendido
                        tot_e -= entregado
                        tot_t -= total

                print("_"*77)
                print("%-20s|%-10s|%-10s|%-12s|%-10s|%-10s|" % ("Total",
                                                    tot_t, tot_v, tot_i, tot_e, tot_f))
            
            print()

    def history(self, cuts):
        hist = self.read_log()
        while True:
            selc = input("\n1 - General\n2 - Personales\n-> ")
            if selc == "1":
                with open(f"{self.path}_names.db") as nm:
                    names = json.load(nm)
                    clothes = {}
                    for name in names.items():
                        for cut in cuts:
                            for cl in name[1][4][cut]:
                                datetime = hist[cl].split()
                                date = [*datetime[0:3],datetime[4]]

                                string_date = " ".join(date)

                                if string_date in clothes:
                                    clothes[string_date].append((datetime[3], cl))
                                else:
                                    clothes[string_date] = [(datetime[3], cl)]
                    
                    self.info_history(clothes) 
            elif selc == "2":
                name = input("\nNombre: ")

                with open(f"{self.path}_names.db") as nm:
                    names = json.load(nm)
                        
                    if name not in names:
                        print("Ese nombre no existe.\n")
                        continue

                    clothes = {}
                
                    for cut in cuts:
                        for cl in names[name][4][cut]:
                            datetime = hist[cl].split()
                            date = [*datetime[0:3],datetime[4]]

                            string_date = " ".join(date)

                            if string_date in clothes:
                                clothes[string_date].append((datetime[3], cl))
                            else:
                                clothes[string_date] = [(datetime[3], cl)]
                
                    self.info_history(clothes) 

            else:
                print()
                break

    def read_log(self):
        with open(f"{self.path}.log") as logfile:
            lines = logfile.readlines()
            history = {}

            for line in lines:
                split = line.split(" -> Prendas vendidas: ")
                clothes = split[1].split()

                for cl in clothes:
                    history[cl] = split[0]
        
        return history              

    def info_history(self, hist):
        for date in hist.items():
            
            print(f"\n{date[0]}:")
            
            print("_"*124)
            print("\n|%-15s|%-7s|%-20s|%-45s|%-10s|%-10s|%-10s|" % ("Hora", "No", "Dueño",
                                                                "Informacion", "Venta", "Costo", "Estado"))
            print("_"*124)
      
            for art in date[1]:
                cl = self.search_article(art[1])

                if cl[1] is not None:
                    print("|%-15s|%-7s|%-20s|%-45s|%-10s|%-10s|%-10s|" %
                        (art[0], art[1], cl[1][3], cl[1][4], cl[1][0], cl[1][1], cl[2]))
            
            print("_"*124)
            print()