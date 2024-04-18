<template>
  <div>
    <h1>Crear nueva relación</h1>
    <form @submit.prevent="crearRelacion">
      <label>
        Etiqueta Nodo 1:
        <select v-model="etiquetaNodo1" @change="obtenerNodos1">
          <option v-for="etiqueta in etiquetas" :key="etiqueta" :value="etiqueta">{{ etiqueta }}</option>
        </select>
      </label>
      <label>
        Nodo 1:
        <select v-model="nodo1">
          <option v-for="nodo in nodos1" :key="nodo.id" :value="nodo.id">{{ nodo.nombre }}</option>
        </select>
      </label>
      <label>
        Etiqueta Nodo 2:
        <select v-model="etiquetaNodo2" @change="obtenerNodos2">
          <option v-for="etiqueta in etiquetas" :key="etiqueta" :value="etiqueta">{{ etiqueta }}</option>
        </select>
      </label>
      <label>
        Nodo 2:
        <select v-model="nodo2">
          <option v-for="nodo in nodos2" :key="nodo.id" :value="nodo.id">{{ nodo.nombre }}</option>
        </select>
      </label>
      <label>
        Tipo de relación:
        <input v-model="tipoRelacion" required>
      </label>
      <div v-for="(valor, nombre) in propiedades" :key="nombre">
        <label>
          {{ nombre }}:
          <input v-model="propiedades[nombre]" required>
        </label>
      </div>
      <button type="submit">Crear relación</button>
    </form>
  </div>
</template>

<script>
import { getSession } from '../Neo4j';

export default {
  data() {
    return {
      etiquetas: [],
      nodos1: [],
      nodos2: [],
      etiquetaNodo1: '',
      etiquetaNodo2: '',
      nodo1: '',
      nodo2: '',
      tipoRelacion: '',
      propiedades: {
        propiedad1: '',
        propiedad2: '',
        propiedad3: '',
      },
    };
  },
  created() {
    this.obtenerEtiquetas();
  },
  methods: {
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
    obtenerNodos1() {
      const session = getSession();
      const query = `MATCH (n:${this.etiquetaNodo1}) RETURN n`;
      session.run(query)
        .then((result) => {
          this.nodos1 = result.records.map(record => record.get('n'));
        })
        .catch((error) => {
          console.error('Error al obtener los nodos:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    obtenerNodos2() {
      const session = getSession();
      const query = `MATCH (n:${this.etiquetaNodo2}) RETURN n`;
      session.run(query)
        .then((result) => {
          this.nodos2 = result.records.map(record => record.get('n'));
        })
        .catch((error) => {
          console.error('Error al obtener los nodos:', error);
        })
        .finally(() => {
          session.close();
        });
    },
    crearRelacion() {
        const session = getSession();
        const query = `
            MATCH (a),(b)
            WHERE ID(a) = toInteger($nodo1) AND ID(b) = toInteger($nodo2)
            CREATE (a)-[r:${this.tipoRelacion} $propiedades]->(b)
            RETURN r
        `;
        const params = {
            nodo1: this.nodo1,
            nodo2: this.nodo2,
            propiedades: this.propiedades,
        };

        session.run(query, params)
            .then((result) => {
                if (result.records.length > 0) {
                    const createdRelation = result.records[0].get('r');
                    console.log('Relación creada con éxito:', createdRelation);
                    alert('Relación creada con éxito!');
                } else {
                    alert('No se pudo crear la relación.');
                }
            })
            .catch((error) => {
            console.error('Error al crear la relación:', error);
            })
            .finally(() => {
            session.close();
            });
    },
  },
};
</script>