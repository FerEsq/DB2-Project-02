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
campos = ['fechaPublicacion', 'comentario', 'recomienda', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fechaP = faker.date_this_century()
        comentario = faker.text(max_nb_chars=100)
        recomienda = random.choice(["true", "false"])
        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(4850, 4969) #Nodo Evento
        filas.append([fechaP, comentario, recomienda, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones PUBLICA".format(n))

generator(800, 'data/relations/publica.csv')