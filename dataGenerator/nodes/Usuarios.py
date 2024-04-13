import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas para estudiantes
"""
* Para estudiantes: 288
* Para catedraticos: 123
"""
seed = 123
Faker.seed(seed)
random.seed(seed)

#Definir los nombres de los campos del archivo CSV
campos = ['nombre', 'apellido', 'edad', 'genero', 'fechaRegistro']

#Función para generar datos aleatorios de usuarios
def usersGenerator(n):
    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        nombre = faker.first_name()
        apellido = faker.last_name()
        edad = random.randint(16, 80)
        genero = random.choice(['Masculino', 'Femenino', 'No especificado'])
        fecha_registro = faker.date_this_century()
        filas.append([nombre, apellido, edad, genero, fecha_registro])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(usersGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} usuarios".format(n))

generator(500, 'data/nodes/catedraticos.csv')