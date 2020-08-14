import json
import time

def log(*args, **kwargs):
    date = time.asctime(time.localtime())

    kwargs.update(dict(file=logfile))
    print(
        f"{date}",
        *args,
        **kwargs,
    )
    logfile.flush()

if __name__ == "__main__":
    names = {}
    logfile = open("./sells.log", "a")

    while True:
        selected = input("1 - Añadir Articulos \n2 - Vender Articulos \n3 - Consultar Caja\n4 - Registro de Ventas\n5 - Buscar Articulos\n6 - Inventario\n7 - Resumen de Ventas Personales\nEnter - Terminar\n-> ")
        print()

        if selected == "1":
            curr_art = 1

            with open("./database.db") as r:
                data = json.load(r)
                curr_art = int(list(data.keys())[-1]) + 1

                while True:
                    name = input("Dueño del articulo: ")
                    if name == "":
                        print()
                        break
                    
                    with open("./names.db") as nm:
                        names = json.load(nm)
                        if name not in names:
                            while True:
                                gain = input("Porciento de ganancia (0-100): ")
                                try:
                                    if gain == "":
                                        gain = 0
                                    elif int(gain) < 0 or int(gain) > 100:
                                        print("Porciento incorrecto")
                                        continue
                                    
                                    names[name] = (0, 0, 0, int(gain), [])
                                    with open("./names.db", "w") as nm:
                                        json.dump(names,nm)

                                    print()
                                    break
                                except:
                                    print("Porciento incorrecto -> (0-100)")
                        else:
                            print()

                        while True:
                            try:
                                info = input(f"Añadir informacion de articulo {curr_art}: ")

                                if not len(info):
                                    print()
                                    break

                                prices = input(f"Añadir precios de articulo {curr_art} (Venta Costo): ").split()
                                
                                sure = input("Confirmar: ")
                                if sure != "":
                                    print("Cancelado\n")
                                    continue

                                try:
                                    if len(prices) == 2:
                                        data[curr_art] = (float(prices[0]), float(prices[1]), False, name, info)
                                    else:
                                        data[curr_art] = (float(prices[0]), float(prices[0]), False, name, info)

                                    print(f"Articulo Añadido Exitosamente \n")

                                    with open("./database.db", "w") as db:
                                        json.dump(data,db)

                                    curr_art += 1
                                except ValueError:
                                    pass
                            except IndexError:
                                print()
                                break

        elif selected == "2":
            while True:
                with open("./database.db") as db:
                    data = json.load(db)

                    clothes = input("Prendas a vender:")
                    clothes = clothes.split()

                    if not len(clothes):
                        print()
                        break

                    tot_price = 0
                    sold = clothes[:]

                    for clothe in clothes:
                        if clothe not in data.keys():
                            sold.remove(clothe)
                            print(f"{clothe} -> No existe")
                        elif data[clothe][2]:
                            sold.remove(clothe)
                            print(f"{data[clothe][4]} -> Ya esta vendido")
                        else:
                            info = data[clothe][4]
                            price = float(data[clothe][0])

                            print(f'{info} -> {price}')
                            tot_price += price
                 
                    print(f"\nPrecio Total: {tot_price}\n")

                    sure = input("Confirmar: ")
                    if(sure == ""):
                        print("OK\n")
                        with open("./names.db",) as nm:
                            names = json.load(nm)
                            
                            for clothe in sold:
                                temp = data[clothe]
                                
                                names[temp[3]][4].append(clothe)
                                names[temp[3]] = (names[temp[3]][0] + 1, names[temp[3]][1] + float(temp[0]), names[temp[3]][2] + float(temp[1]) - float(temp[1])*names[temp[3]][3]/100 , names[temp[3]][3], names[temp[3]][4])

                                data[clothe] = (temp[0], temp[1], True, temp[3], temp[4])

                            if len(sold):
                                log("-> Prendas vendidas:",*clothes)

                            with open("./database.db", "w") as dw:
                                json.dump(data,dw)

                            with open("./names.db", "w") as nm:
                                json.dump(names,nm)
                    else:
                        print("Cancelado\n")

        elif selected == '3':
            with open("./database.db") as db:
                with open("./names.db") as nm:

                    names = json.load(nm)
                    data = json.load(db)
                    total = 0
                    cant = 0
                    total_gan = 0
                    total_dar = 0
                    sold_out = []           

                    print("\n%-17s%-13s%-10s%-10s%-10s%-10s" % ("Nombres","Cantidad","Total", "Entregar", "Ganancia", "Prendas Vendidas"))
                    print("_"*80)
                    
                    for name in names.items():            
                        cant += name[1][0]
                        total += name[1][1]
                        total_gan += name[1][1] - name[1][2]
                        total_dar += name[1][2]
                        sold_out.extend(name[1][4])

                        print("%-20s%-10s%-10s%-10s%-10s" % (name[0], name[1][0], name[1][1], name[1][2], name[1][1] - name[1][2]), *name[1][4])
                        

                    print("_"*80)
                    print("%-20s%-10s%-10s%-10s%-10s" % ("General",cant,total,total_dar,total_gan), *sold_out)
                    print()
        
        elif selected == '4':

            with open("./sells.log", 'r') as s:
                [print(line[:-1]) for line in s.readlines()]

            print()
            
        elif selected == '5':
            search = input("Prendas a Localizar: ")
            search = search.split()

            with open("./database.db") as db:
                data = json.load(db)

                for clothe in search:
                    if clothe not in data.keys():
                        print(f"{clothe}: No existe")
                    elif data[clothe][2]:
                        info = data[clothe][4]
                        name = data[clothe][3]
                        price = float(data[clothe][0])
                        print(f"{clothe}: {info} - {name} (Vendido) -> {price}")
                    else:
                        info = data[clothe][4]
                        name = data[clothe][3]
                        price = float(data[clothe][0])

                        print(f'{clothe}: {info} - {name} (Sin Vender) -> {price}')

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
                        print(f"{cl[1][4]} -> {cl[1][1]}")
                        total += cl[1][1]
                
                print(f"\nTotal: {total} \n")
        else:
            break
