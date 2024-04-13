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

//Importar salones aulas
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/salonesAulas.csv' AS row
CREATE (s:Salon:Aula {
    codigo: row.codigo,
    capacidad: toInteger(row.capacidad),
    disponible: row.disponible = 'true',
    edificio: row.edificio,
    nivel: toInteger(row.nivel)
})
RETURN s;

//Importar salones laboratorios
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/salonesLaboratorios.csv' AS row
CREATE (s:Salon:Laboratorio {
    codigo: row.codigo,
    capacidad: toInteger(row.capacidad),
    disponible: row.disponible = 'true',
    edificio: row.edificio,
    nivel: toInteger(row.nivel)
})
RETURN s;

//Importar clubes artisticos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/clubesArtisticos.csv' AS row
CREATE (c:Club:Artistico {
    nombre: row.nombre,
    miembros: toInteger(row.miembros),
    presupuesto: toInteger(row.presupuesto),
    fechaFundacion: date(row.fechaFundacion)
})
SET c.dias = [dia IN split(row.dias, ';') | trim(dia)]
RETURN c;

//Importar clubes deportivos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/clubesDeportivos.csv' AS row
CREATE (c:Club:Deportivo {
    nombre: row.nombre,
    miembros: toInteger(row.miembros),
    presupuesto: toInteger(row.presupuesto),
    fechaFundacion: date(row.fechaFundacion)
})
SET c.dias = [dia IN split(row.dias, ';') | trim(dia)]
RETURN c;

//Importar clubes academicos
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/nodes/clubesAcademicos.csv' AS row
CREATE (c:Club:Academico {
    nombre: row.nombre,
    miembros: toInteger(row.miembros),
    presupuesto: toInteger(row.presupuesto),
    fechaFundacion: date(row.fechaFundacion)
})
SET c.dias = [dia IN split(row.dias, ';') | trim(dia)]
RETURN c;

//Importar relaciones INTERACTUA
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/interactua.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:INTERACTUA {
    fechaUltimaInteraccion: date(row.fechaUltimaInteraccion),
    tipoInteraccion: row.tipoInteraccion,
    frecuencia: toInteger(row.frecuencia)
    }]->(e)
RETURN r

//Importar relaciones PUBLICA
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/publica.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:PUBLICA {
    fechaPublicación: date(row.fechaPublicación),
    comentario: row.comentario,
    recomienda: row.recomienda = 'true'
    }]->(e)
RETURN r

//Importar relaciones ASISTE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/asiste.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ASISTE {
    motivo: row.motivo,
    confirmado: row.confirmado = 'true',
    rol: row.rol   
    }]->(e)
RETURN r

//Importar relaciones ORGANIZA
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/organiza.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ORGANIZA {
    fechaOrganizacion: date(row.fechaOrganizacion),
    responsabilidades: split(row.responsabilidades, ';'),
    puntuacion: toInteger(row.puntuacion) 
    }]->(e)
RETURN r

//Importar relaciones IMPARTE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/imparte.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:IMPARTE {
    fechaInicio: date(row.fechaInicio),
    fechaFin: date(row.fechaFin),
    semestre: toInteger(row.semestre) 
    }]->(e)
RETURN r

//Importar relaciones CURSA
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/cursa.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:CURSA {
    año: toInteger(row.año),
    semestre: toInteger(row.semestre),
    nota: toFloat(row.nota)
    }]->(e)
RETURN r

//Importar relaciones PERTENECE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/pertenece.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:PERTENECE {
    desde: date(row.desde),
    activo: row.activo = 'true',
    rol: row.rol
    }]->(e)
RETURN r

//Importar relaciones ESTA_EN Usuarios
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/estaenUsuario.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ESTA_EN {
    fecha: date(row.fecha),
    tipoOcupacion: row.tipoOcupacion,
    autorizado: row.autorizado = 'true'
    }]->(e)
RETURN r

//Importar relaciones ESTA_EN Clubes
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/estaenClub.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ESTA_EN {
    fecha: date(row.fecha),
    tipoOcupacion: row.tipoOcupacion,
    autorizado: row.autorizado = 'true'
    }]->(e)
RETURN r

//Importar relaciones ES_MIEMBRO
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/esmiembro.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ES_MIEMBRO {
    fechaInscipcion: date(row.fechaInscipcion),
    status: row.status,
    frecuencia: toInteger(row.frecuencia)
    }]->(e)
RETURN r

//Importar relaciones OCUPA
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/ocupa.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:OCUPA {
    dias: split(row.dias, ';'),
    horaInicio: row.horaInicio,
    horaFin: row.horaFin
    }]->(e)
RETURN r

//Importar relaciones ES_DE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/esde.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:ES_DE {
    desde: date(row.desde),
    nuevo: row.nuevo = 'true',
    activo: row.activo = 'true'
    }]->(e)
RETURN r

//Importar relaciones REALIZA Facultades
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/realizaFacultad.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:REALIZA {
    objetivo: row.objetivo,
    importancia: row.importancia,
    recurrente: row.recurrente = 'true'
    }]->(e)
RETURN r

//Importar relaciones REALIZA Clubes
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/FerEsq/DB2-Project-02/main/data/relations/realizaClub.csv' AS row
MATCH (s)
WHERE id(s) = toInteger(row.nodoInicio)
MATCH (e)
WHERE id(e) = toInteger(row.nodoFin)
CREATE (s)-[r:REALIZA {
    objetivo: row.objetivo,
    importancia: row.importancia,
    recurrente: row.recurrente = 'true'
    }]->(e)
RETURN r