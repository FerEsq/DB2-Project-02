<template>
  <div>
    <h1 class="title">Editar Nodo</h1>
    <div v-if="Object.keys(nodeProperties).length > 0">
      <form @submit.prevent="saveChanges">
        <div v-for="(value, key) in nodeProperties" :key="key" class="form-group">
          <label :for="key" class="property">{{ key }}</label>
          <input type="text" :id="key" v-model="nodeProperties[key]" class="form-control" />
          <button class="delete" @click.prevent="deleteProperty(key)">
              <svg class="trash" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff">
                <path d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
        </div>
        <button type="submit" class="save">Guardar</button>
      </form>
    </div>
    <div v-else>
      <p class="charging">Cargando propiedades del nodo...</p>
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
    deleteProperty(propertyName) {
        // Prevenir la inyección de Cypher asegurándose de que propertyName es un nombre de propiedad válido
        if (!propertyName.match(/^[a-zA-Z_][a-zA-Z0-9_]*$/)) {
            console.error('Nombre de propiedad inválido para eliminación:', propertyName);
            return;
        }

        const session = getSession();
        const numericId = parseInt(this.id);
        // Utiliza la interpolación de cadenas para incluir el nombre de la propiedad de forma segura.
        const query = `MATCH (n) WHERE ID(n) = $id SET n.${propertyName} = NULL RETURN n`;

        session
            .run(query, { id: numericId })
            .then(() => {
            // Elimina la propiedad del objeto local después de una eliminación exitosa
            delete this.nodeProperties[propertyName];
            })
            .catch(error => {
            console.error('Error al eliminar la propiedad:', error);
            })
            .finally(() => {
            session.close();
            });
        },

  },
};
</script>

<style>
.form-group {
  margin-bottom: 1rem;
  width: 100%;
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

.charging {
  border-collapse: collapse;
  margin-top: 1rem;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 20px;
  margin-left: 1%;
  font-weight: bold;
  color: #226946;
  margin-bottom: 2%;
}

.property{
  display: block !important;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1%;
  color: #226946;
}

.form-control {
  display: inline-block !important;
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

.delete {
  display: inline-block !important;
  padding: 7px 10px;
  margin-left: 1%;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #D52941 !important;
  color: white !important;
}

.trash {
  height: 1em; /* O el tamaño que prefieras */
  width: 1em; /* Mantén la misma altura y ancho para preservar la proporción */
}
</style>
