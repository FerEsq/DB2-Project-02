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
campos = ['fechaOrganizacion', 'responsabilidades', 'puntuacion', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):
    
    responsabilidades = [
        "Planificacion",
        "Coordinacion",
        "Promocion",
        "Logistica",
        "Comunicacion",
        "Gestion de presupuesto",
        "Seguridad",
        "Contratacion",
        "Programacion",
        "Evaluacion"
    ]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fechaOrganizacion = faker.date_this_century()
        responsabilidad = random.sample(responsabilidades, 5)
        responsabilidadParsed = '"' + ";".join(responsabilidad) + '"'
        puntuacion = random.randint(1, 10)

        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(4850, 4969) #Nodo Evento
        filas.append([fechaOrganizacion, responsabilidadParsed, puntuacion, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones ORGANIZA".format(n))

generator(800, 'data/relations/organiza.csv')