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

def add_article():
     with open("./database.db") as r:
        data = json.load(r)
        curr_art = int(list(data.keys())[-1]) + 1

        while True:
            name = input("Dueño del articulo: ")
            if name == "":
                print()
                return
            
            if name not in names:
                add_name(name)
            else:
                print()
            
            while True:
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
                except:
                    print("Los datos introducidos son incorrectos. Cancelado\n")
                    pass
                
def add_name(name):
    with open("./names.db") as nm:
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
                with open("./names.db", "w") as nm:
                    json.dump(names,nm)

                print()
                break
            except:
                print("Porciento incorrecto -> (0-100)")

def sell_article():
    while True:
        clothes = input("Prendas a vender:")
        clothes = clothes.split()

        if not len(clothes):
            print()
            return

        tot_price = 0
        sold = clothes[:]

        for clothe in clothes:
            art = search_article(clothe)

            if art[0]:
                price = float(art[1][0])
                tot_price += price
                
            print(art[2])
                        
        print(f"\nPrecio Total: {tot_price}\n")

        sure = input("Confirmar: ")

        if(sure == ""):
            print("OK\n")

            with open("./database.db") as db:
                data = json.load(db)
                
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


def search_article(art):
    with open("./database.db") as db:
        data = json.load(db)

        try:
            info = data[art][4]
            name = data[art][3]
            price = float(data[art][0])
            if data[art][2]:
                return (False, data[art], f"{clothe}: {name} - {info} -> {price} (Vendido)")
            else:
                return (True, data[art], f"{clothe}: {name} - {info} -> {price}")
                
        except:
            return (False, None, f"{art}: No existe")

def resume():
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

def print_log():
    with open("./sells.log", 'r') as s:
        [print(line[:-1]) for line in s.readlines()]
