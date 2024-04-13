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
campos = ['dias', 'horaInicio', 'horaFin', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        dias = random.choice(["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"])
        horaInicio = random.randint(0, 23)
        horaFin = random.randint(horaInicio, 23)

        nodoInicio = random.randint(4500, 4849) #Nodo Curso
        nodoFin = random.randint(4977, 5156) #Nodo Salon
        filas.append([dias, horaInicio, horaFin, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones OCUPA".format(n))

generator(100, 'data/relations/ocupa.csv')