LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/estudiantes.csv' AS row
CREATE (u:Usuario:Estudiante {
    nombre: row.nombre,
    apellido: row.apellido,
    edad: toInteger(row.edad),
    genero: row.genero,
    fechaRegistro: date(row.fechaRegistro)
})
RETURN u;

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/catedraticos.csv' AS row
CREATE (u:Usuario:Catedratico {
    nombre: row.nombre,
    apellido: row.apellido,
    edad: toInteger(row.edad),
    genero: row.genero,
    fechaRegistro: date(row.fechaRegistro)
})
RETURN u;

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/cursosPresenciales.csv' AS row FIELDTERMINATOR ','
CREATE (c:Curso:Presencial{
    nombre: row.nombre,
    codigo: row.codigo,
    creditos: toInteger(row.creditos),
    promedioAprobado: toFloat(row.promedioAprobado)
})
SET c.competencias = [competencia IN split(row.competencias, ';') | trim(competencia)]
RETURN c;

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/cursosVirtuales.csv' AS row FIELDTERMINATOR ','
CREATE (c:Curso:Virtual{
    nombre: row.nombre,
    codigo: row.codigo,
    creditos: toInteger(row.creditos),
    promedioAprobado: toFloat(row.promedioAprobado)
})
SET c.competencias = [competencia IN split(row.competencias, ';') | trim(competencia)]
RETURN c;

