import json
import time


def log(path, *args, **kwargs):
    date = time.asctime(time.localtime())

    kwargs.update(dict(file=path))
    print(
        f"{date}",
        *args,
        **kwargs,
    )
    logfile.flush()


def create_path(name, venta):
    return f'./{name}_{venta}'


def add_article(path):
    with open(f"{path}.db") as r:
        data = json.load(r)
        curr_art = int(list(data.keys())[-1]) + 1

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
                                prices[1]), False, name, info)
                        else:
                            data[curr_art] = (float(prices[0]), float(
                                prices[0]), False, name, info)

                        print(f"Articulo Añadido Exitosamente \n")

                        with open(f"{path}.db", "w") as db:
                            json.dump(data, db)

                        curr_art += 1
                    except:
                        print("Los datos introducidos son incorrectos. Cancelado\n")
                        pass


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

                names[name] = (0, 0, 0, int(gain), [])
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

                        names[temp[3]][4].append(clothe)
                        names[temp[3]] = (names[temp[3]][0] + 1, names[temp[3]][1] + float(temp[0]), names[temp[3]][2] + float(
                            temp[1]) - float(temp[1])*names[temp[3]][3]/100, names[temp[3]][3], names[temp[3]][4])

                        data[clothe] = (temp[0], temp[1],
                                        True, temp[3], temp[4])

                    if len(sold):
                        log(f"{path}.log", "-> Prendas vendidas:", *clothes)

                    with open(f"{path}.db", "w") as dw:
                        json.dump(data, dw)

                    with open(f"{path}_names.db", "w") as nm:
                        json.dump(names, nm)
        else:
            print("Cancelado\n")


def search_article(path, art):
    with open(f"{path}.db") as db:
        data = json.load(db)

        try:
            info = data[art][4]
            name = data[art][3]
            price = float(data[art][0])
            if data[art][2]:
                return (False, data[art], f"{art}: {name} - {info} -> {price} (Vendido)")
            else:
                return (True, data[art], f"{art}: {name} - {info} -> {price}")

        except:
            return (False, None, f"{art}: No existe")


def resume(path):
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
                cant += name[1][0]
                total += name[1][1]
                total_gan += name[1][1] - name[1][2]
                total_dar += name[1][2]
                sold_out.extend(name[1][4])

                print("%-20s%-10s%-10s%-10s%-10s" %
                      (name[0], name[1][0], name[1][1], name[1][2], name[1][1] - name[1][2]), *name[1][4])

            print("_"*80)
            print("%-20s%-10s%-10s%-10s%-10s" %
                  ("General", cant, total, total_dar, total_gan), *sold_out)
            print()


def print_log(path):
    with open(f"{path}.log") as s:
        [print(line[:-1]) for line in s.readlines()]


def create_sales(name):
    with open("./users.db") as us:
        users = json.load(us)

        while True:
            venta = input("\nNombre su venta: ")
            if venta == "":
                print("Nombre no valido, intente con uno diferente")
                continue
            elif venta in users[name]:
                print("Nombre existente, intente con uno diferente")
                continue
            else:
                users[name].append(venta)

            with open(f"./{name}_{venta}.db", "w") as db:
                json.dump({}, db)

            with open(f"./{name}_{venta}.log", "w") as log:
                json.dump({}, log)

            with open(f"./{name}_{venta}_names.db", "w") as names:
                json.dump({}, names)

            with open("./users.db", "w") as user:
                json.dump(users, user)
                        
            print("Venta creada exitosamente. \n")
            break

def temp(name, venta):
    while True:
        selected = input("\n1 - Añadir Articulos \n2 - Vender Articulos \n3 - Resumen\n4 - Registro de Ventas\n5 - Buscar Articulos\n6 - Inventario\n7 - Resumen de Ventas Personales\nEnter - Cerrar Sesion\n-> ")
        print()

        if selected == "1":
            add_article(create_path(name, venta))

        elif selected == "2":
            sell_article(create_path(name, venta))

        elif selected == '3':
            resume(create_path(name, venta))

        elif selected == '4':
            print_log(create_path(name, venta))
            print()

        elif selected == '5':
            search = input("Prendas a Localizar: ")
            search = search.split()

            for clothe in search:
                print(search_article(create_path(name, venta), clothe)[2])

            print()

        elif selected == '6':

            select = input(
                "1 - Añadir prenda\n2 - Revisar faltantes\n3 - Resumen por nombres\n->")
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
                                    print(
                                        f"{clothe}: -> Ya esta en inventario")
                                else:
                                    inven[clothe] = True
                                    info = data[clothe][4]
                                    price = float(data[clothe][0])

                                    print(
                                        f'{clothe}: -> Añadido {info} - {data[clothe][3]} -> {price}')
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

                        [print(f'{clothe}: -> {data[clothe][4]} - {data[clothe][3]} -> {float(data[clothe][0])} Vendido->{data[clothe][2]}')
                         for clothe in lost]

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