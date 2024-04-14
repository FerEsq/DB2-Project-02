<template>
  <div>
    <h1 class="title">Editar Nodo</h1>
    <div v-if="Object.keys(nodeProperties).length > 0">
      <form @submit.prevent="saveChanges">
        <div v-for="(value, key) in nodeProperties" :key="key" class="form-group">
          <label :for="key" class="property">{{ key }}</label>
          <input type="text" :id="key" v-model="nodeProperties[key]" class="form-control" />
        </div>
        <button type="submit" class="save">Guardar</button>
      </form>
    </div>
    <div v-else>
      <p>Cargando datos del nodo...</p>
    </div>
  </div>
</template>

<script>
import { getSession } from '../Neo4j'; // Asegúrate de que este sea el camino correcto para tu configuración

export default {
  name: 'EditarNodo',
  props: {
    id: {
      type: Number, // O String, dependiendo del tipo de dato que sea el ID
      required: true
    }
  },
  data() {
    return {
      nodeProperties: {}, // Aquí se almacenarán las propiedades del nodo
    };
  },
  created() {
    console.log('El ID recibido es:', this.id);
    this.fetchNode();
  },
  methods: {
    fetchNode() {
      const session = getSession();
      const numericId = parseInt(this.id);
      session
        .run('MATCH (n) WHERE ID(n) = $id RETURN properties(n) as properties', { id: numericId })
        .then(result => {
          if (result.records.length > 0) {
            this.nodeProperties = result.records[0].get('properties');
          } else {
            console.error('No se encontró el nodo con el ID: ', numericId);
            // Manejar el caso de no encontrar el nodo aquí
          }
        })
        .catch(error => {
          console.error('Error al buscar el nodo:', error);
          // Manejar el error aquí
        })
        .finally(() => {
          session.close();
        });
    },
    saveChanges() {
        const session = getSession();
        // Construir un objeto con las propiedades que se van a actualizar
        const numericId = parseInt(this.id);
        const params = { id: numericId, ...this.nodeProperties };

        // Construir la consulta Cypher para actualizar las propiedades del nodo
        let query = 'MATCH (n) WHERE ID(n) = $id SET ';
        query += Object.keys(this.nodeProperties)
                        .map(key => `n.${key} = $${key}`)
                        .join(', ');

        // Ejecutar la consulta Cypher con los parámetros
        session
            .run(query, params)
            .then(() => {
            // Aquí manejas el caso de éxito, como mostrar una notificación al usuario
            // o redirigirlo a otra página
            this.$router.push('/usuario'); // Reemplaza esto con tu ruta deseada
            })
            .catch(error => {
            // Aquí manejas el caso de error, como mostrar un mensaje de error al usuario
            console.error('Error al guardar los cambios:', error);
            })
            .finally(() => {
            session.close(); // Asegúrate de cerrar la sesión cuando hayas terminado
            });
    },
  },
};
</script>

<style>
.form-group {
  margin-bottom: 1rem;
}

.title {
  border-collapse: collapse;
  margin-top: 1rem;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 30px;
  margin-left: 1%;
  font-weight: bold;
  color: #226946;
  margin-bottom: 2%;
}

.property{
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1%;
  color: #226946;
}

.form-control {
  width: 85.5% !important;
  margin-left: 1% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.save {
  margin-top: 1rem;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1%;
  font-weight: bold;
  padding: 11px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #226946;
  color: white;
  margin-bottom: 2%;
}
</style>
