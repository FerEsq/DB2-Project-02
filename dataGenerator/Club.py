import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas para cursos
"""
* Para artisticos: 288
* Para deportivos: 123
* Para academicos: 321
"""
seed = 321
Faker.seed(seed)
random.seed(seed)

#Definir los nombres de los campos del archivo CSV
campos = ['nombre', 'miembros', 'presupuesto', 'dias', 'fechaFundacion']

#Función para generar datos aleatorios de usuarios
def clubsGenerator(n):
    
    # clubes = [ "Teatro", "Danza", "Coro", "Fotografia", "Dibujo", "Escultura", "Pintura", "Musica", "Cine"]
    # clubes = [ "Futbol", "Basloncesto", "Volleybal", "Ajedrez", "Tenis de mesa", "Natacion", "Atletismo", "Gimnasia"]
    clubes = [ "Debate", "Emprendimiento", "Lengua de Señas", "Voluntariado", "Astronomia", "Robotica", "Cocina"]


    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        nombre = random.choice(clubes)
        clubes.remove(nombre)
        miembros = random.randint(5, 50)
        presupuesto = random.randint(1000, 10000)
        dias = random.sample(["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"], 3)
        diasParsed = '"' + ";".join(dias) + '"'
        fechaFundacion = faker.date_this_century()
        filas.append([nombre, miembros, presupuesto, diasParsed, fechaFundacion])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(clubsGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} clubes".format(n))

generator(5, 'data/clubesAcademicos.csv')