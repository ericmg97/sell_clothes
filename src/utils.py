import json
import time


def log(path, *args, **kwargs):
    date = time.asctime(time.localtime())
    logfile = open(path,"a")
    kwargs.update(dict(file=logfile))
    print(
        f"{date}",
        *args,
        **kwargs,
    )
    logfile.flush()
    logfile.close()

def create_path(name, venta):
    return f'./{name}_{venta}'

def add_article(path):
    with open(f"{path}.db") as r:
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

            with open(f"{path}_names.db") as nm:
                names = json.load(nm)

                if name not in names:
                    add_name(path, name)
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

                        with open(f"{path}.db", "w") as db:
                            json.dump(data, db)

                        curr_art += 1
                    except:
                        print("Los datos introducidos son incorrectos. Cancelado\n")
                        pass

def change_prices(path):
    while True:
        art = input("Numero de serie: ")
        print()
        
        if art == "":
            print()
            break

        cl = search_article(path,art)

        with open(f"{path}.db") as r:
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

                    with open(f"{path}.db", "w") as db:
                        json.dump(data, db)

                except:
                    print("Los datos introducidos son incorrectos. Cancelado\n")
                    pass
            else:
                print(cl[2])
                print("No se pueden modificar sus precios\n")

def add_name(path, name):
    with open(f"{path}_names.db") as nm:
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
                with open(f"{path}_names.db", "w") as nm:
                    json.dump(names, nm)

                print()
                break
            except:
                print("Porciento incorrecto -> (0-100)")

def sell_article(path):
    while True:
        clothes = input("Prendas a vender:")
        clothes = clothes.split()

        if not len(clothes):
            print()
            return

        tot_price = 0
        sold = clothes[:]

        for clothe in clothes:
            art = search_article(path, clothe)

            if art[0]:
                price = float(art[1][0])
                tot_price += price

            print(art[2])

        print(f"\nPrecio Total: {tot_price}\n")

        sure = input("Confirmar: ")

        if(sure == ""):
            print("OK\n")

            with open(f"{path}.db") as db:
                data = json.load(db)

                with open(f"{path}_names.db",) as nm:
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
                        log(f"{path}.log", "-> Prendas vendidas:", *clothes)

                    with open(f"{path}.db", "w") as dw:
                        json.dump(data, dw)

                    with open(f"{path}_names.db", "w") as nm:
                        json.dump(names, nm)
        else:
            print("Cancelado\n")

def return_article(path): #terminar
    pass

def resume(path): #mejorar
    while(True):
        sel = input("Cortes a resumir: ")
        if sel == "":
            print()
            return

        try:
            cuts = {int(x) - 1 for x in sel.split()}
        except:
            print("Cortes inexistentes\n")

        with open(f"{path}.db") as db:
            with open(f"{path}_names.db") as nm:
                names = json.load(nm)
                data = json.load(db)
                    
                total = 0
                cant = 0
                total_gan = 0
                total_dar = 0
                sold_out = []

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

def create_sales(name):
    with open("./users.db") as us:
        users = json.load(us)

        while True:
            venta = input("\nNombre su venta: ")
            if venta == "":
                print("Nombre no valido, intente con uno diferente")
                continue
            elif name not in users:
                users[name] = [venta]
            elif venta in users[name]:
                print("Nombre existente, intente con uno diferente")
                continue
            else:
                users[name].append(venta)

            path = create_path(name,venta)

            with open(f"{path}.db", "w") as db:
                json.dump({}, db)

            with open(f"{path}.log", "w") as log:
                json.dump({}, log)

            with open(f"{path}_names.db", "w") as names:
                json.dump({}, names)

            with open("./users.db", "w") as user:
                json.dump(users, user)
                        
            print("Venta creada exitosamente. \n")
            break

def inventory(path): 
    while True:
        opt = input("1 - Realizar Inventario\n2 - Revisar faltantes \n3 - Entregar ropa al dueño\n4 - Borrar Inventario\n-> ")
        print()
        
        if opt == "1":
            while True:
                ad = input("Añadir prenda: ")
                if ad == "":
                    print()
                    break
                else:
                    list_art = ad.split()
                    ad_art = []
                    for art in list_art:
                        search = search_article(art)
                        if search[0]:
                            ad_art.append(art)
                            
                        print(search[2])
                    
                    sure = input("Seguro: ")
                    if sure == "":
                        with open(f"{path}.db") as db:
                            data = json.load(db)

                            for cl in ad_art:
                                data[cl][6] = True

                            with open(f"{path}.db", "w") as d:
                                json.dump(data, d)

                        print("Prendas añadidas correctamente. \ns")
                    else:
                        print("Cancelado.\n")
                        continue
        elif opt == "2":        
            with open(f"{path}.db") as db:
                data = json.load(db)
                
                lost = []
                filter = input("Nombre: ")
                if filter == "todos":
                    for cl in data.items():
                        if cl[1][5] and not cl[1][6]:
                            lost.append(cl[0])
                else:
                    try:
                        for cl in data.items():
                            if cl[1][5] and not cl[1][6] and cl[1][3] == filter:
                                lost.append(cl[0])
                    except:
                        pass

                if not len(lost):
                    print("Todo en orden")

                [print(f'{clothe}: {data[clothe][3]} - {data[clothe][4]} -> {float(data[clothe][0])} Vendido->{data[clothe][2]}')
                    for clothe in lost]

                print()             
        elif opt == "3":
            owner = input("Nombre: ")
            if owner == "":
                continue

            with open(f"{path}.db") as db:
                data = json.load(db)
                change = False
                for cl in data:
                    if data[cl][3] == owner:
                        change = True
                        data[cl][5] = False

                with open(f"{path}.db", "w") as d:
                    json.dump(data, d)
            if change:
                print("Ropa entregada correctamente.\n")
            else:
                print("Dueño no encontrado en la lista. \n")

        elif opt == "4":
            sure = input("Estas serguro: ")
            
            if sure == "":
                with open(f"{path}.db") as db:
                    data = json.load(db)

                    for cl in data:
                        if data[cl][5] and not data[cl][2]:
                            data[cl][6] = False
                    
                    with open(f"{path}.db", "w") as d:
                        json.dump(data,d)
                
                print("Inventario borrado correctamente. \n")
            else:
                print("Cancelado. \n")

        else:
            print()
            return

def advanced_search(path): #terminar
    while True:
        typ = input("1 - Busqueda por numero de serie\n2 - Busqueda por nombre\n-> ")
        print()

        if typ == "1":
            search = input("Prendas a Localizar: ")
            search = search.split()

            for clothe in search:
                print(search_article(path, clothe)[2])

            print()
        elif typ == "2":
            pass #implementar busqueda por nombre
        else:
            return

def search_article(path, art):
    with open(f"{path}.db") as db:
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

def make_cut(path):
    sure = input("Estas seguro: ")
    if sure == "":
        with open(f"{path}_names.db") as nm:
            names = json.load(nm)

            for name in names:
                names[name][0].append(0)
                names[name][1].append(0)
                names[name][2].append(0)
                names[name][4].append([])

            with open(f"{path}_names.db", "w") as n:
                json.dump(names,n)

            print(f"Corte {len(names[name][0]) - 1} cerrado")
        
    else:
        print("Cancelado\n")

def temp(name, venta):
    while True:
        selected = input("\n1 - Articulos\n2 - Inventario \n3 - Organizacion de venta\n4 - Resumen por nombres\nEnter - Cerrar Sesion\n-> ")
        print()
        
        path = create_path(name,venta)

        if selected == "1":
            opt = input("1 - Añadir \n2 - Vender \n3 - Cambiar Precios \n4 - Devolucion \n5 - Buscar \n-> ")
            print()
            
            if opt == "1":
                add_article(path)
            
            elif opt == "2":
                sell_article(path)

            elif opt == '3':
                change_prices(path)  

            elif opt == '4':
                return_article(path)

            elif opt == '5':
                advanced_search(path)
       
        
        elif selected == '2':
            inventory(path)

        elif selected == "3":
            sel = input("1 - Realizar Corte \n2 - Resumen de ventas \n-> ")
            print()
            
            if sel == "1":
                make_cut(path)
            elif sel == "2":
                resume(path)
            
        elif selected == '4': #organizar y terminar

            select = input(
                "3 - Resumen por nombres\n->")
            print()

            if select == '3':
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

                            print("\n%-19s%-8s%-10s%-12s%-10s" % ("Nombres",
                                                                  "Total", "Vendido", "Inventario", "Perdido"))
                            print("_"*62)

                            for name in rep_name.items():
                                total = name[1]
                                vendido = names[name[0]][0]
                                inventario = rep_inv[name[0]]
                                perdido = total - vendido - inventario

                                print("%-20s%-10s%-10s%-12s%-10s" %
                                      (name[0], total, vendido, inventario, perdido))

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