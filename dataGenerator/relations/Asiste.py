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
campos = ['motivo', 'confirmado', 'rol', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):
    
    roles = [
        "Organizador", "Orador", "Asistente", "Patrocinador",
        "Moderador", "Voluntario", "Panelista",
        "Presentador", "Expositor", "Facilitador"
    ]


    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        motivo = faker.text(max_nb_chars=100)
        confirmado = random.choice(["true", "false"])
        rol = random.choice(roles)

        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(4850, 4969) #Nodo Evento
        filas.append([motivo, confirmado, rol, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones ASISTE".format(n))

generator(800, 'data/relations/asiste.csv')