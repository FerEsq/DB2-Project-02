import csv
import random
from faker import Faker

#Crear una instancia de Faker para generar datos aleatorios
faker = Faker()

#Establecer las semillas para cursos
Faker.seed(288)
random.seed(288)

#Definir los nombres de los campos del archivo CSV
campos = ['nombre', 'codigo', 'creditos', 'promedioAprobado', 'competencias']

#Función para generar combinaciones únicas de topics y números
def namesGenerator(temas, ids, filas):
    while True:
        #Seleccionar un topic y un número aleatoriamente
        tema = random.choice(temas)
        id = random.choice(ids)
        
        #Crear la combinación
        combinacion = f"{tema} {id}"
        
        if not any(combinacion in fila for fila in filas):
            return combinacion 

#Función para generar datos aleatorios de usuarios
def coursesGenerator(n):
    #Definir los temas y los identificadores para los nombres de los cursos
    # temas = [
    #     'Introduccion', 'Avanzado', 'Programacion', 'Diseno', 'Marketing',
    #     'Negocios', 'Matematicas', 'Ciencias', 'Historia', 'Literatura',
    #     'Fotografia', 'Musica', 'Idiomas', 'Finanzas', 'Robotica',
    #     'Arquitectura', 'Psicologia', 'Salud', 'Nutricion', 'Deporte',
    #     'Arte', 'Moda', 'Cocina', 'Tecnologia', 'Ambientacion'
    # ]

    # temas = [
    #     'Animacion', 'Economia', 'Fisica', 'Quimica', 'Geografia',
    #     'Cine', 'Filosofia', 'Sociologia', 'Politica', 'Religion'
    # ]

    temas = [
        'Educacion', 'Comunicacion', 'Derecho', 'Arqueologia', 'Biologia',
        'Antropologia', 'Geologia', 'Astronomia', 'Ecologia', 'Veterinaria',
        'Pintura', 'Escultura', 'Teatro', 'Danza', 'Literatura'
    ]

    identificadores = ['101', '201', '301', '102', '202', '302', '103', '203', '303']

    cursos = [tema + ' ' + identificador for tema in temas for identificador in identificadores]

    competencias = [
        "Pensamiento critico",
        "Resolucion de problemas",
        "Comunicacion efectiva",
        "Trabajo en equipo",
        "Liderazgo",
        "Capacidad de investigacion",
        "Habilidades analiticas",
        "Adaptabilidad",
        "Gestion del tiempo",
        "Etica profesional",
        "Creatividad",
        "Habilidades interpersonales",
        "Conciencia global",
        "Autodisciplina",
        "Toma de decisiones informada"
    ]

    #Generar n filas de datos aleatorios
    filas = []
    for _ in range(n):
        nombre = random.choice(cursos)
        cursos.remove(nombre)
        codigo = nombre[:3] + nombre[-3:]
        creditos = random.randint(1,10)
        promedioAprobado = round(random.uniform(0, 100), 2)
        competencias = random.sample(competencias, 5)
        competenciasParsed = '"' + ";".join(competencias) + '"'

        filas.append([nombre, codigo, creditos, promedioAprobado, competenciasParsed])

    return filas

def generator(n, filename):
    with open(filename, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, quoting=csv.QUOTE_NONE, escapechar='\\', quotechar='')
        escritor.writerow(campos)  #Escribir la fila de encabezado
        escritor.writerows(coursesGenerator(n))  #Escribir las filas de datos

    print("Se generaron {} cursos".format(n))

generator(100, 'data/cursosHibridos.csv')