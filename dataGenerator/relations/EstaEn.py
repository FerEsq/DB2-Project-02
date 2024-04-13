import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas para cursos
seed = 288
Faker.seed(seed)
random.seed(seed)

#Definir los nombres de los campos del archivo CSV
campos = ['fecha', 'tipoOcupacion', 'autorizado', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    ocupaciones = [
        "Clases",
        "Reuniones",
        "Conferencias",
        "Examenes",
        "Talleres",
        "Presentaciones",
        "Seminarios",
        "Entrevistas",
        "Practicas"
    ]


    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fecha = faker.date_this_century()
        tipo = random.choice(ocupaciones)
        autorizado = random.choice(["true", "false"])

        # nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoInicio = random.randint(5157, 5171) #Nodo Club
        nodoFin = random.randint(4977, 5156) #Nodo Salon
        filas.append([fecha, tipo, autorizado, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones ESTA_EN".format(n))

generator(100, 'data/relations/estaenClub.csv')