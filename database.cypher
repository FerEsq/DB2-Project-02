//Importar usuarios estudiantes
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/estudiantes.csv' AS row
CREATE (u:Usuario:Estudiante {
    nombre: row.nombre,
    apellido: row.apellido,
    edad: toInteger(row.edad),
    genero: row.genero,
    fechaRegistro: date(row.fechaRegistro)
})
RETURN u;

//Importar usuarios catedraticos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/catedraticos.csv' AS row
CREATE (u:Usuario:Catedratico {
    nombre: row.nombre,
    apellido: row.apellido,
    edad: toInteger(row.edad),
    genero: row.genero,
    fechaRegistro: date(row.fechaRegistro)
})
RETURN u;

//Importar cursos presenciales
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/cursosPresenciales.csv' AS row FIELDTERMINATOR ','
CREATE (c:Curso:Presencial{
    nombre: row.nombre,
    codigo: row.codigo,
    creditos: toInteger(row.creditos),
    promedioAprobado: toFloat(row.promedioAprobado)
})
SET c.competencias = [competencia IN split(row.competencias, ';') | trim(competencia)]
RETURN c;

//Importar cursos virtuales
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/cursosVirtuales.csv' AS row FIELDTERMINATOR ','
CREATE (c:Curso:Virtual{
    nombre: row.nombre,
    codigo: row.codigo,
    creditos: toInteger(row.creditos),
    promedioAprobado: toFloat(row.promedioAprobado)
})
SET c.competencias = [competencia IN split(row.competencias, ';') | trim(competencia)]
RETURN c;

//Importar cursos hibridos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/cursosHibridos.csv' AS row FIELDTERMINATOR ','
CREATE (c:Curso:Hibrido{
    nombre: row.nombre,
    codigo: row.codigo,
    creditos: toInteger(row.creditos),
    promedioAprobado: toFloat(row.promedioAprobado)
})
SET c.competencias = [competencia IN split(row.competencias, ';') | trim(competencia)]
RETURN c;

//Importar eventos presenciales
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/eventosPresenciales.csv' AS row
CREATE (e:Evento:Presencial {
    titulo: row.titulo,
    descripcion: row.descripcion,
    fechaInicio: date(row.fechaInicio),
    fechaFin: date(row.fechaFin),
    participantes: toInteger(row.participantes)
})
RETURN e;

//Importar eventos virtuales
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/eventosVirtuales.csv' AS row
CREATE (e:Evento:Virtual {
    titulo: row.titulo,
    descripcion: row.descripcion,
    fechaInicio: date(row.fechaInicio),
    fechaFin: date(row.fechaFin),
    participantes: toInteger(row.participantes)
})
RETURN e;

//Importar eventos hibridos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/eventosHibridos.csv' AS row
CREATE (e:Evento:Hibrido {
    titulo: row.titulo,
    descripcion: row.descripcion,
    fechaInicio: date(row.fechaInicio),
    fechaFin: date(row.fechaFin),
    participantes: toInteger(row.participantes)
})
RETURN e;

//Importar facultades
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/facultades.csv' AS row
CREATE (f:Facultad {
    nombre: row.nombre,
    miembros: toInteger(row.miembros),
    fechaCreacion: date(row.fechaCreacion),
    oficina: row.oficina
})
SET f.carreras = [carrera IN split(row.carreras, ';') | trim(carrera)]
RETURN f;




