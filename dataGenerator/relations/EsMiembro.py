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
campos = ['fechaInscipcion', 'status', 'frecuencia', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    roles = ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Vocal", "Miembro"]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fechaInscripcion = faker.date_this_century()
        status = random.choice(roles)
        frecuencia = random.randint(1, 7)

        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(5157, 5171) #Nodo Club
        filas.append([fechaInscripcion, status, frecuencia, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones ES_MIEMBRO".format(n))

generator(800, 'data/relations/esmiembro.csv')