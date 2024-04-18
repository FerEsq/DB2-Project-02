<template>
  <div>
    <h1 class="subtitle">Gestión de Relaciones</h1>
    <div>
      <label>Tipo de Nodo:</label>
      <select v-model="tipoNodo" @change="obtenerNodos">
        <option v-for="tipo in tiposNodo" :key="tipo" :value="tipo">{{ tipo }}</option>
      </select>
      <label>Nodo:</label>
      <select v-model="nodoSeleccionado" @change="obtenerTiposRelaciones">
        <option v-for="nodo in nodos" :key="nodo.id" :value="nodo.id">{{ nodo.nombre }}</option>
      </select>
      <label>Tipo de Relación:</label>
      <select v-model="tipoRelacion" @change="obtenerRelaciones">
        <option v-for="relacion in tiposRelacion" :key="relacion" :value="relacion">{{ relacion }}</option>
      </select>
    </div>
    <table v-if="relaciones.length > 0" class="table-relaciones">
      <thead>
        <tr>
          <th>Relación</th>
          <th>Propiedades</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(relacion, index) in relaciones" :key="index" :class="{ 'eliminar': relacionesEliminar.includes(relacion) }">
          <td>{{ index + 1 }}</td>
          <td>
            <div v-for="(propiedad, nombre) in relacion.properties" :key="nombre">
              <label>{{ nombre }}:</label>
              <input :type="obtenerTipoInput(propiedad)" v-model="relacion.properties[nombre]" />
            </div>
          </td>
          <td>
            <button class="save" @click="agregarPropiedad(relacion)">+</button>
            <button class="delete" @click="relacionAEliminar(relacion)">
              <svg class="trash" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff">
                  <path d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <button class="save" @click="guardarCambios" :disabled="!nodoSeleccionado || relacionesEliminar.length === 0">Guardar Cambios</button>
  </div>
</template>

<script>
import { getSession } from '../Neo4j';

export default {
  data() {
    return {
      tipoNodo: '',
      nodoSeleccionado: null,
      tiposNodo: [],
      tiposRelacion: [],
      nodos: [],
      tipoRelacion: '',
      relaciones: [],
      relacionesEliminar: [],
    };
  },
  created() {
    this.obtenerTiposNodo();
  },
  methods: {
    obtenerTipoInput(valor) {
      const regexFecha = /^\d{4}-\d{2}-\d{2}$/;
      if (typeof valor === 'number' || !isNaN(valor.low)) {
        return 'number';
      } else if (typeof valor === 'boolean') {
        return 'checkbox';
      } else if (regexFecha.test(valor)) {
        return 'date';
      } else {
        return 'text';
      }
    },
    obtenerTiposNodo() {
      const session = getSession();
      const query = 'CALL db.labels()';
      session.run(query)
        .then((result) => {
          this.tiposNodo = result.records.map(record => record.get(0));
          this.nodoSeleccionado = null;
        })
        .catch((error) => {
          console.error('Error al obtener los tipos de nodo:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    obtenerNodos() {
      const session = getSession();
      const query = `MATCH (n:${this.tipoNodo}) RETURN n`;
      session.run(query)
        .then((result) => {
          this.nodos = result.records.map(record => {
            const nodo = record.get('n');
            return {
              id: nodo.identity.toNumber(),
              nombre: nodo.properties.nombre, // asumiendo que tus nodos tienen una propiedad 'nombre'
            };
          });
        })
        .catch((error) => {
          console.error('Error al obtener los nodos:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    obtenerTiposRelaciones() {
      const session = getSession();
      const query = `MATCH (n)-[r]->() WHERE ID(n) = toInteger($idNodo) RETURN DISTINCT TYPE(r) as tipoRelacion`;
      const params = { idNodo: this.nodoSeleccionado };
      session.run(query, params)
        .then((result) => {
          this.tiposRelacion = result.records.map(record => {
            return record.get('tipoRelacion');
          });
        })
        .catch((error) => {
          console.error('Error al obtener las relaciones:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    obtenerRelaciones() {
      const session = getSession();
      const query = `MATCH (n)-[r]->() WHERE ID(n) = toInteger($idNodo) RETURN r`;
      const params = { idNodo: this.nodoSeleccionado };
      session.run(query, params)
        .then((result) => {
          this.relaciones = result.records.map(record => {
            return record.get('r');
          });
        })
        .catch((error) => {
          console.error('Error al obtener las relaciones:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    agregarPropiedad(relacion) {
      relacion.propiedades['nueva_propiedad'] = '';
    },
    relacionAEliminar(relacion) {
      const index = this.relacionesEliminar.indexOf(relacion);
      if (index === -1) {
        this.relacionesEliminar.push(relacion);
      } else {
        this.relacionesEliminar.splice(index, 1);
      }
    },
    guardarCambios() {
      
      
      // Eliminar relaciones
      this.relacionesEliminar.forEach((relacion) => {
        const session = getSession();
        const partesElementId = relacion.elementId.split(':');
        const idRelacion = partesElementId[2];
        const query = `MATCH (a)-[r]->(b) WHERE ID(r) = toInteger($idRelation) DELETE r`;
        const params = { idRelation: idRelacion };
        session.run(query, params)
          .then(() => {
            console.log('Relación eliminada con éxito');
          })
          .catch((error) => {
            console.error('Error al eliminar la relación:', error);
          });
      });
    
    }
  }
};
</script>

<style scoped>
.eliminar {
  background-color: #ffcccc; /* Cambia esto al color que prefieras */
}

.table-relaciones {
  width: 100%;
  border-collapse: collapse;
}

.table-relaciones th, .table-relaciones td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table-relaciones th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}

.subtitle {
  border-collapse: collapse;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 20px;
  /*margin-left: 1%;*/
  font-weight: 900;
  color: #226946;
}

.page-text{
  display: block !important;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  /*margin-left: 1%;*/
  color: #226946;
}

.text-elements {
  display: inline-block !important;
  height: 40px !important;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.text-properties {
  display: inline-block !important;
  width: 94% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.save {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1.5% !important;
  font-weight: bold;
  padding: 11px 10px !important;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #226946;
  color: white;
  margin-bottom: 2%;
  display: inline-block !important;
}

.save:disabled {
  background-color: #ABC4AB;
  cursor: not-allowed;
}

.no-save {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1.5% !important;
  font-weight: bold;
  padding: 11px 10px !important;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #D52941 !important;
  color: white;
  margin-bottom: 2%;
  display: inline-block !important;
}

.no-save:disabled {
  background-color: #ABC4AB;
}

div {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.botoncitos {
  display: inline-block !important;
  margin: 0px;
  padding: 0px;
  border: 0px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

h1 {
  font-size: 24px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 10px;
}

input {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

</style>
