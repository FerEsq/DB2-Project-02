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
campos = ['fechaUltimaInteraccion', 'tipoInteraccion', 'frecuencia', 'nodoInicio', 'nodoFin']

#Función para generar datos aleatorios de usuarios
def relationsGenerator(n):
    
    interacciones = [
        "Seguir", "Enviar mensaje", "Comentar publicacion", "Dar like",
        "Etiquetar", "Compartir publicacion", "Responder comentario",
        "Bloquear", "Agregar amigo", "Videollamada"
    ]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        fechaUI = faker.date_this_century()
        interaccion = random.choice(interacciones)
        frecuencia = random.randint(1, 10)
        nodoInicio = random.randint(0, 4499) #Nodo Usuario
        nodoFin = random.randint(0, 4499) #Nodo Usuario
        filas.append([fechaUI, interaccion, frecuencia, nodoInicio, nodoFin])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(relationsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} relaciones INTERACTUA".format(n))

generator(800, 'data/relations/interactua.csv')