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
campos = ['fechaInicio', 'fechaFin', 'semestre', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fechaInicio = faker.date_this_century()
        fechaFin = faker.date_this_century()
        semestre = random.randint(1, 2)

        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(4500, 4849) #Nodo Curso
        filas.append([fechaInicio, fechaFin, semestre, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones IMPARTE".format(n))

generator(800, 'data/relations/imparte.csv')