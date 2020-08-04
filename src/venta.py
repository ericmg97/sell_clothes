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
        selected = input("1 - Añadir Articulos \n2 - Vender Articulos \n3 - Consultar Caja\n4 - Registro de Ventas\nEnter - Terminar\n-> ")
        if selected == "1":
            curr_art = 1

            with open("./database.db") as r:
                data = json.load(r)
                curr_art = len(data) + 1

                while True:
                    name = input("Dueño del articulo:")
                    if name == "":
                        break
                    
                    with open("./names.db") as nm:
                        names = json.load(nm)
                        if name not in names:
                            while True:
                                gain = input("Porciento de ganancia (0-100) :")
                                try:
                                    if gain == "":
                                        gain = 0
                                    elif int(gain) < 0 or int(gain) > 100:
                                        print("Prociento incorrecto")
                                        continue
                                    
                                    names[name] = (0, 0, 0, int(gain), [])
                                    with open("./names.db", "w") as nm:
                                        json.dump(names,nm)
                                    break
                                except:
                                    print("Porciento incorrecto -> (0-100)")

                        while True:
                            try:
                                prices = input(f"Añadir precios de articulo {curr_art} (Venta, Costo):").split()
                                try:
                                    if len(prices) == 2:
                                        data[curr_art] = (int(prices[0]), int(prices[1]), False, name)
                                    else:
                                        data[curr_art] = (int(prices[0]), int(prices[0]), False, name)

                                    with open("./database.db", "w") as db:
                                        json.dump(data,db)

                                    curr_art += 1
                                except ValueError:
                                    pass
                            except IndexError:
                                break

        elif selected == "2":
            while True:
                with open("./database.db") as db:
                    data = json.load(db)

                    clothes = input("Prendas a vender:")
                    clothes = clothes.split()

                    if not len(clothes):
                        break

                    tot_price = 0
                    
                    for clothe in clothes:
                        if clothe not in data.keys():
                            print(f"{clothe} No existe")
                            clothes.remove(clothe)
                        elif data[clothe][2]:
                            print(f"{clothe} Ya esta vendido")
                            clothes.remove(clothe)
                        else:
                            tot_price += float(data[clothe][0])
                 
                    print(f"Precio Total: {tot_price}")

                    sure = input("Confirmar: ")
                    if(sure == ""):
                        print("OK")
                        for clothe in clothes:
                            temp = data[clothe]
                            data[clothe] = (temp[0], temp[1], True, temp[3])

                        if len(clothes):
                            log("-> Prendas vendidas:",*clothes)

                        with open("./database.db", "w") as dw:
                            json.dump(data,dw)

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
                    for no, clothe in enumerate(data.values(), 1):
                        if clothe[2]:
                            total += float(clothe[0])
                            sold_out.append(no)
                            names[clothe[3]][4].append(no)
                            names[clothe[3]] = (names[clothe[3]][0] + 1, names[clothe[3]][1] + float(clothe[0]), names[clothe[3]][2] + float(clothe[1]), names[clothe[3]][3], names[clothe[3]][4])
                            cant += 1

                    print("\n%-17s%-13s%-10s%-10s%-10s%-10s" % ("Nombres","Cantidad","Total", "Entregar", "Ganancia", "Prendas Vendidas"))
                    print("_"*80)
                    for name in names.items():            
                        total_gan += name[1][1] - name[1][2] + name[1][2]*name[1][3]/100
                        total_dar += name[1][2] - name[1][2]*name[1][3]/100
                        print("%-20s%-10s%-10s%-10s%-10s" % (name[0], name[1][0], name[1][1], name[1][2] - name[1][2]*name[1][3]/100, name[1][1] - name[1][2] + name[1][2]*name[1][3]/100), *name[1][4])
                        

                    print("_"*80)
                    print("%-20s%-10s%-10s%-10s%-10s" % ("General",cant,total,total_dar,total_gan), *sold_out)
                    print()
        
        elif selected == '4':

            print()
            with open("./sells.log", 'r') as s:
                [print(line[:-1]) for line in s.readlines()]

            print()
            
        else:
            break