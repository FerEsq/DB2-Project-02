<template>
    <div>
      <h1>Crear nueva relación</h1>
      <form @submit.prevent="crearRelacion">
        <label>
          Nodo de origen:
          <input type="text" :value="nodoOrigen" disabled>
        </label>
        <label>
          Etiqueta Nodo destino:
          <select v-model="etiquetaNodoDestino" @change="obtenerNodosDestino">
            <option v-for="etiqueta in etiquetas" :key="etiqueta" :value="etiqueta">{{ etiqueta }}</option>
          </select>
        </label>
        <label>
          Nodo destino:
          <select v-model="nodoDestino">
            <option v-for="nodo in nodosDestino" :key="nodo.id" :value="nodo.identity.low">{{ nodo.identity.low }}</option>
          </select>
        </label>
        <label>
          Tipo de relación:
          <select v-model="tipoRelacion">
            <option v-for="relacion in relaciones" :key="relacion" :value="relacion">{{ relacion }}</option>
          </select>
        </label>
        <div v-for="(valor, nombre, index) in propiedades" :key="nombre" class="props">
            <label>
                <input type="text" v-model="Object.keys(propiedades)[index]" required>
                <input :type="obtenerTipoInput(valor)" v-model="propiedades[nombre]" step="any" required>
            </label>
        </div>
        <div v-for="(propiedad, index) in nuevasPropiedades" :key="index">
            <input type="text" v-model="propiedad.key" placeholder="Nombre de la propiedad">
            <input type="text" v-model="propiedad.value" placeholder="Valor de la propiedad">
            <button @click.prevent="eliminarPropiedad(index)">
                <svg class="trash" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff">
                    <path d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>

        <button @click.prevent="agregarPropiedad">Agregar propiedad</button>
        <button type="submit" :disabled="!hayCambios">{{ textoBoton }}</button>
      </form>
      <button v-if="relacionInicial" @click="mostrarDialogoEliminar = true">Eliminar relación</button>
      <div v-if="mostrarDialogoEliminar">
        ¿Estás seguro de que quieres eliminar esta relación?
        <button @click="eliminarRelacion">Aceptar</button>
        <button @click="mostrarDialogoEliminar = false">Cancelar</button>
      </div>
    </div>
  </template>

<script>
import { getSession } from '../Neo4j';

export default {
  props: ['nodoOrigen', 'relacionInicial'],
  data() {
    return {
      etiquetas: [],
      nodosDestino: [],
      etiquetaNodoDestino: '',
      nodoDestino: '',
      tipoRelacion: '',
      relaciones: [],
      propiedades: {},
      nuevasPropiedades: [],
      propiedadesIniciales: {},
      mostrarDialogoEliminar: false,
    };
  },
  computed: {
    textoBoton() {
      return this.relacionInicial ? 'Guardar cambios' : 'Crear relación';
    },
    hayCambios() {
      return JSON.stringify(this.propiedades) !== JSON.stringify(this.propiedadesIniciales) || this.nuevasPropiedades.length > 0;
    },
  },
  created() {
    this.obtenerEtiquetas();
    this.obtenerRelaciones();
    if (this.relacionInicial) {
      // console.log('Relación inicial:', this.relacionInicial.relation.elementId);
      this.etiquetaNodoDestino = this.relacionInicial.relatedNode.labels[0];
      this.nodoDestino = this.relacionInicial.relatedNode.identity.low;
      this.tipoRelacion = this.relacionInicial.relation.type;
      this.propiedades = this.relacionInicial.relation.properties;
      this.propiedadesIniciales = { ...this.propiedades };
      this.obtenerNodosDestino();
    }
  },
  methods: {
    eliminarRelacion() {
      const session = getSession();
      const partesElementId = this.relacionInicial.relation.elementId.split(':');
      const idRelacion = partesElementId[2];
      
      const query = `MATCH (a)-[r]->(b) WHERE ID(r) = toInteger($idRelation) DELETE r`;
      const params = { idRelation: idRelacion };

      session.run(query, params)
        .then(() => {
          alert('Relación eliminada con éxito!');
          location.reload();
        })
        .catch((error) => {
          console.error('Error al eliminar la relación:', error);
          alert('No se pudo eliminar la relación.');
        });
    },
    agregarPropiedad() {
      this.nuevasPropiedades.push({ key: '', value: '' });
    },
    eliminarPropiedad(index) {
      this.nuevasPropiedades.splice(index, 1);
    },
    obtenerEtiquetas() {
      const session = getSession();
      const query = 'CALL db.labels()';
      session.run(query)
        .then((result) => {
          this.etiquetas = result.records.map(record => record.get(0));
        })
        .catch((error) => {
          console.error('Error al obtener las etiquetas:', error);
        })
        .finally(() => {
          session.close();
        });
    },
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
    obtenerNodosDestino() {
      const session = getSession();
      const query = `MATCH (n:${this.etiquetaNodoDestino}) RETURN n`;
      session.run(query)
        .then((result) => {
          this.nodosDestino = result.records.map(record => {
            return record.get('n')});
        })
        .catch((error) => {
          console.error('Error al obtener los nodos:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    obtenerRelaciones() {
      const session = getSession();
      const query = 'CALL db.relationshipTypes()';
      session.run(query)
        .then((result) => {
          this.relaciones = result.records.map(record => record.get(0));
        })
        .catch((error) => {
          console.error('Error al obtener las relaciones:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    crearRelacion() {
    if (!this.nodoOrigen || !this.nodoDestino) {
        alert('Por favor, selecciona los nodos de origen y destino.');
        return;
    }

    if (!this.tipoRelacion) {
        alert('Por favor, selecciona el tipo de relación.');
        return;
    }

    if (this.nuevasPropiedades.length < 3) {
        alert('Por favor, agregar mínimo 3 propiedades.');
        return;
    }

    const session = getSession();
    let propertiesObject = { ...this.propiedades };
    this.nuevasPropiedades.forEach((prop) => {
        if (prop.key.trim() && prop.value.trim()) {
        propertiesObject[prop.key.trim()] = prop.value.trim();
        }
    });

    const query = `
        MATCH (a),(b)
        WHERE ID(a) = toInteger($nodoOrigen) AND ID(b) = toInteger($nodoDestino)
        CREATE (a)-[r:${this.tipoRelacion} $properties]->(b)
        RETURN r
    `;
    const params = {
        nodoOrigen: this.nodoOrigen,
        nodoDestino: this.nodoDestino,
        properties: propertiesObject,
    };

    session.run(query, params)
        .then((result) => {
        if (result.records.length > 0) {
            const createdRelation = result.records[0].get('r');
            console.log('Relación creada con éxito:', createdRelation);
            alert('Relación creada con éxito!');
            // location.reload();
        } else {
            alert('No se pudo crear la relación.');
        }
        })
        .catch((error) => {
        console.error('Error al crear la relación:', error);
        alert('Hubo un error al crear la relación.');
        })
        .finally(() => {
        session.close();
        });
    },
  },
};
</script>

<style scoped>
div {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007BFF;
  color: white;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
}

</style>
