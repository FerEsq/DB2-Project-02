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
campos = ['objetivo', 'importancia', 'recurrente', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        objetivo = faker.text(max_nb_chars=100)
        importancia = random.choice(["Alta", "Media", "Baja"])
        recurrente = random.choice(["true", "false"])

        # nodoInicio = random.randint(4970, 4976) #Nodo Facultad
        nodoInicio = random.randint(5157, 5171) #Nodo Club
        nodoFin = random.randint(4850, 4969) #Nodo Evento
        filas.append([objetivo, importancia, recurrente, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones REALIZA".format(n))

generator(100, 'data/relations/realizaClub.csv')