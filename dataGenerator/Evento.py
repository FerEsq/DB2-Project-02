import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas 
"""
* Para presenciales: 288
* Para virtuales: 123
* Para hibridos: 321
"""
seed = 321
Faker.seed(seed)
random.seed(seed)

#Definir los nombres de los campos del archivo CSV
campos = ['titulo', 'descripcion', 'fechaInicio', 'fechaFin', 'participantes']

#Función para generar datos aleatorios de usuarios
def eventsGenerator(n):
    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        titulo = faker.word().capitalize() + " " + faker.word().capitalize() + " " + faker.word().capitalize()
        descripcion = faker.text(max_nb_chars=100)
        fechaInicio = faker.date_this_century()
        fechaFin = faker.date_this_century()
        participantes = random.randint(100, 5000)

        filas.append([titulo, descripcion, fechaInicio, fechaFin, participantes])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(eventsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} eventos".format(n))

generator(60, 'data/eventosHibridos.csv')