import os
import csv

data_dic = []

#Carga la informacion del archivo .csv (Base de datos)
with open('synergy_logistics_database.csv', 'r') as data_db:
    data = csv.DictReader(data_db)
        
    for data_row in data :
        data_dic.append(data_row);

#Limpia la consola dependiendo del sistema operativo
def clearConsole():
    command = 'clear' # para MacOS
    if os.name in ('nt', 'dos'):   
        command = 'cls'  #para windows
    os.system(command)

#suma el valor total de la exportacion, importacion o ambas en una lista por modo de transporte
def get_list_transport_mode(direction, withDirection) :
        #rutas
        transport_list =  []
        transports  =  []
       
        for data_row in data_dic : 
            
            if(data_row["direction"] == direction or not withDirection) : #Filtra por dirección (importacion o exportacion)
                transport_row = [
                    ('transport_mode', data_row['transport_mode']), 
                            ]
                if transport_row not in transports : #valida si el transporte ya esta en la lista
                    #Agrega el transporte en la lista con el valor total de la E. , I. , o ambas
                    transports.append(transport_row)
                    transport_row_copy = transport_row.copy()
                    transport_row_copy.append(('total', int(data_row['total_value'])))
                    transport_list.append(dict(transport_row_copy))
                else :
                    for transport in transport_list : #Busca en la lista el transporte
                        if transport['transport_mode'] == data_row['transport_mode'] :
                            #suma el nuevo valor total de la I, E, o ambas
                            transport['total'] += int(data_row['total_value'])

        transport_list.sort(reverse = True, key = lambda x:x['total'])
        return transport_list

#cuenta las exportaciones, importaciones o ambas en una lista por rutas(origen, destino)
def get_list_routes_with_total(direction , withDirection) :
        #rutas
        routes_list =  []
        routes =  []
       
        for data_row in data_dic : 
            
            if(data_row["direction"] == direction or not withDirection) :  #Filtra por dirección (importacion o exportacion)
                route_row = [
                    ('origin', data_row['origin']), 
                    ('destination', data_row['destination'])
                            ]
                if route_row not in routes : #valida si la ruta ya esta en la lista
                    #Agrega la ruta en la lista
                    routes.append(route_row)
                    route_row_copy = route_row.copy()
                    route_row_copy.append(('total', 1))
                    routes_list.append(dict(route_row_copy))
                else :
                    for route_export in  routes_list : #Busca la ruta en la lista
                        if(route_export['origin'] == data_row['origin'] 
                                and route_export['destination'] == data_row['destination']) :
                                route_export['total'] += 1 #Aumenta el contador de I, E o ambas en 1

        routes_list.sort(reverse = True, key = lambda x:x['total'])
        return routes_list

#imprime en consola los paises y los porcentajes de la lista, corata la impresion hasta la suma de un porcentaje dado
def get_list_countrys_in_porcent(porcent, list_porcent, withPorcent) : 

    aux = 1
    total_porcent = 0
    if withPorcent :
        print(f'\nPaises que representan el {porcent} % o más \n')
    for row in list_porcent :
        if(total_porcent < porcent or not withPorcent):
            total_porcent += row['porcent']
            print(f"{aux}._Pais {row['country']} - porcentaje {row['porcent']}")
            aux += 1
    
    print(f"\nPorcentaje que represntan {total_porcent}% \n")

def get_list_porcent_by_country(total_value, direction, withDirection) :
    countrys = []
    countrys_list = []

    for data_row in data_dic :
        if data_row['direction'] == direction or not withDirection : #Filtra por Exportacion, importacion o ambas
            country_row = [('country', data_row['origin'])]
            if country_row not in countrys:
                #Agrega el pais a la lista
                countrys.append(country_row)
                country_row_copy = country_row.copy()
                country_row_copy.append(('total', int(data_row['total_value'])))
                countrys_list.append(dict(country_row_copy))
            else:
                for country_row  in countrys_list : #Busca el pais en la lista
                    if country_row['country'] == data_row['origin'] :
                        #suma el nuevo valor total 
                       country_row['total'] += int(data_row['total_value'])
    
    for country_row in countrys_list : 
        #recorre la lista y calcula los porcentajes por pais
        porcent = ( country_row['total'] * 100 ) / total_value
        country_row['porcent'] = round(porcent, 3)
    
    countrys_list.sort(reverse = True, key = lambda x:x['porcent'])
    return countrys_list

#suma todos los valores totales de las Exportaciones e importaciones
def get_calculate_total_value() :
    total_value = 0    
    for data_row in data_dic:
        total_value += int(data_row['total_value'])

    return total_value

# muestre el analisis de la opcion 1
def show_option_one() :
        clearConsole()
        route_exports_list = get_list_routes_with_total('Exports',True)
        route_imports_list = get_list_routes_with_total('Imports',True)
        route_total_list = get_list_routes_with_total('Imports',False)

        print("Opción 1 : Rutas más demandadas \n")

        print("+-+-+-+-+-+-+-+ Rutas de Exportación más demandadas +-+-+-+-+-+-+-+ \n")
        aux = 1
        for route in route_exports_list :
            print(f"{aux}._ Origen: {route['origin']} - Destino: {route['destination']} - Total Exportaciones : {route['total']}")
            aux += 1
            if aux == 11 :
                break

        print("\n\n+-+-+-+-+-+-+-+ Rutas de Importación más demandadas +-+-+-+-+-+-+-+ \n")
        aux = 1
        for route in route_imports_list :
            print(f"{aux}._ Origen: {route['origin']} - Destino: {route['destination']} - Total Importaciones : {route['total']}")
            aux += 1
            if aux == 11 :
                break

        print("\n\n+-+-+-+-+-+-+-+ Rutas de Importación y Exportación más demandadas +-+-+-+-+-+-+-+ \n")
        aux = 1
        for route in route_total_list :
            print(f"{aux}._ Origen: {route['origin']} - Destino: {route['destination']} - Total Importaciones : {route['total']}")
            aux += 1
            if aux == 11 :
                break

        input('\n\nPresiona enter para regresar al menu principal')
   
# muestre el analisis de la opcion 2
def show_option_two():
    clearConsole()
    transport_exports_list = get_list_transport_mode('Exports', True)
    transport_imports_list = get_list_transport_mode('Imports' , True )
    transport_total_list = get_list_transport_mode('__', False)

    print("Opción 2 : Medios de transporte utilizados por valor de exportaciones e importaciones \n")

    print("+-+-+-+-+-+-+-+ Valor total de exportaciones por medio de transporte +-+-+-+-+-+-+-+ \n")
    aux = 1
    for transport in transport_exports_list :
        print(f"{aux}._ Medio de transporte {transport['transport_mode']} - Valor total de las exportaciones : {transport['total']}")
        aux += 1
        
    print("\n\n +-+-+-+-+-+-+-+ Valor total de importaciones por medio de transporte +-+-+-+-+-+-+-+ \n")
    aux = 1
    for transport in transport_imports_list :
        print(f"{aux}._ Medio de transporte {transport['transport_mode']} - Valor total de las importaciones : {transport['total']}")
        aux += 1
    
    print("\n\n +-+-+-+-+-+-+-+Valor total de importaciones y exportaciones por medio de transporte +-+-+-+-+-+-+-+ \n")
    aux = 1
    for transport in transport_total_list :
        print(f"{aux}._ Medio de transporte {transport['transport_mode']} - Valor total de las importaciones y exportaciones: {transport['total']}")
        aux += 1

    input('\n\nPresiona enter para regresar al menu principal')

# muestre el analisis de la opcion 3
def show_option_three():

    clearConsole()
    total_value = get_calculate_total_value()

    list_porcent_exports = get_list_porcent_by_country(total_value, 'Exports', True)
    list_porcent_imports = get_list_porcent_by_country(total_value, 'Imports', True)
    country_porcent_total_list = get_list_porcent_by_country(total_value, '__', False)
    
    print("Opción 3 : Valor total de importaciones y exportaciones (porcentajes) \n")

    print('+-+-+-+-+-+-+-+ Porcentajes de exportaciones por pais +-+-+-+-+-+-+-+\n')
    get_list_countrys_in_porcent(0, list_porcent_exports, False )

    print('\n\n+-+-+-+-+-+-+-+ Porcentajes de importaciones por pais +-+-+-+-+-+-+-+ \n')
    get_list_countrys_in_porcent(0, list_porcent_imports, False)
      
    print('\n\n +-+-+-+-+-+-+-+ Porcentajes de importaciones y exportaciones por pais +-+-+-+-+-+-+-+\n') 
    get_list_countrys_in_porcent(80, country_porcent_total_list, True) 

    input('\n\nPresiona enter para regresar al menu principal')

def show_menu() :

    clearConsole()

    print("""Synergy Logistics
    
    1._ Opcion 1
    2._ Opcion 2
    3._ Opcion 3 
    4._ Salir

    """)

    option_selected = input("Elige una opción: ")

    while(option_selected != "4") :
        if option_selected == "1" :
            clearConsole()
            show_option_one()
            show_menu()
            break
        elif option_selected == "2" :
            clearConsole()
            show_option_two()
            show_menu()
            break
        elif option_selected == "3" :
            clearConsole()
            show_option_three()
            show_menu()
            break
        else :
            clearConsole()

            print("""Synergy Logistics
        
            1._ Opcion 1
            2._ Opcion 2
            3._ Opcion 3 
            4._ Salir

            """)

            option_selected = input("Elige una opción correcta: ")

#inicia la aplicacion
def init():  
    show_menu()
