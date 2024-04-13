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
campos = ['desde', 'activo', 'rol', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    roles = [
        "Profesor",
        "Investigador",
        "Decano",
        "Tutor",
        "Coordinador",
        "Director",
        "Asistente",
        "Consejero",
        "Evaluador",
        "Mentor"
    ]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        desde = faker.date_this_century()
        activo = random.choice(["true", "false"])
        rol = random.choice(roles)

        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(4970, 4976) #Nodo Facultad
        filas.append([desde, activo, rol, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones PERTENECE".format(n))

generator(800, 'data/relations/pertenece.csv')