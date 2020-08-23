from utils import *

if __name__ == "__main__":
    names = {}
    logfile = open("./sells.log", "a")

    while True:
        selected = input("1 - Añadir Articulos \n2 - Vender Articulos \n3 - Resumen\n4 - Registro de Ventas\n5 - Buscar Articulos\n6 - Inventario\n7 - Resumen de Ventas Personales\nEnter - Terminar\n-> ")
        print()

        if selected == "1":
            add_article()
           
        elif selected == "2":
            sell_article()

        elif selected == '3':
            resume()
        
        elif selected == '4':
            print_log()
            print()
            
        elif selected == '5':
            search = input("Prendas a Localizar: ")
            search = search.split()

            for clothe in search:
                print(search_article(clothe)[2])
            
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
                    
