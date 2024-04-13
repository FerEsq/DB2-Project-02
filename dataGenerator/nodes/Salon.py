import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas para cursos
"""
* Para aulas: 288
* Para labs: 123
"""
seed = 123
Faker.seed(seed)
random.seed(seed)

#Definir los nombres de los campos del archivo CSV
campos = ['id', 'capacidad', 'disponible', 'edificio', 'nivel']

#Función para generar datos aleatorios de usuarios
def salonsGenerator(n):
    
    #edificios = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'CIT']
    edificios = ['A', 'B', 'C']

    niveles = ['1', '2', '3', '4', '5', '6', '7']

    #cursos = [tema + ' ' + identificador for tema in temas for identificador in identificadores]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        edificio = random.choice(edificios)
        nivel = random.choice(niveles)
        id = edificio + "-" + nivel + str(random.randint(10,99))
        capacidad = random.randint(20, 40)
        disponible = random.choice(["true", "false"])
        filas.append([id, capacidad, disponible, edificio, nivel])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(salonsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} salones".format(n))

generator(30, 'data/nodes/salonesLaboratorios.csv')