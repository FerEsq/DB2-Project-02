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
            <div v-for="(property, index) in newProperties" :key="index" class="form-group new-property">
                <input
                type="text"
                placeholder="Nombre de la propiedad"
                v-model="property.key"
                class="form-control new-property-name"
                />
                <button class="delete" @click.prevent="deleteTextbox(index)">
                    <svg class="trash" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff">
                        <path d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <input
                type="text"
                placeholder="Valor de la propiedad"
                v-model="property.value"
                class="form-control new-property-value"
                />
            </div>
            <button @click.prevent="addNewProperty" class="save">Añadir propiedad</button>

        <div class="form-group">
          <label for="applyToNodes" class="changes"> * Aplicar cambios a los siguientes nodos:</label>
          <select v-model="applyToNodes" id="applyToNodes" class="multiple-nodes">
            <option v-for="num in 11" :key="num" :value="num - 1" >
              {{ num - 1 }}
            </option>
          </select>
        </div>
        <button type="submit" class="save">Guardar</button>
      </form>
    </div>
    <div v-else>
      <p class="charging">Cargando propiedades del nodo...</p>
    </div>
    <div class="relations-group">
      <div v-for="(relacion, index) in relaciones" :key="index">
        <h1 class="title">Editar relación {{ index + 1 }}</h1>
        <crear-relacion :nodo-origen="id" :relacion-inicial="relacion"></crear-relacion>
      </div>
      <h1 class="title">Agregar nueva relación</h1>
      <crear-relacion :nodo-origen="id"></crear-relacion>
    </div>
  </div>
</template>

<script>
import { getSession } from '../Neo4j'; // Asegúrate de que este sea el camino correcto para tu configuración
import AgregarRelacion from '@/components/AgregarRelacion.vue';

export default {
  name: 'EditarNodo',
  components: {
    'crear-relacion': AgregarRelacion,
  },
  props: {
    id: {
      type: Number, // O String, dependiendo del tipo de dato que sea el ID
      required: true
    }
  },
  data() {
    return {
      nodeProperties: {}, // Aquí se almacenarán las propiedades del nodo
      newProperties: [],
      applyToNodes: 0, // Para guardar el número seleccionado del dropdown
      relaciones: [], // Aquí se almacenarán las relaciones del nodo
    };
  },
  created() {
    console.log('El ID recibido es:', this.id);
    this.fetchNode();
    this.fetchNode();
    this.fetchRelations();
  },
  methods: {
    fetchRelations() {
      const session = getSession();
      const query = `
        MATCH (a)-[r]->(m)
        WHERE ID(a) = toInteger($id)
        RETURN r,m
      `;
      const params = {
        id: this.id,
      };

      session.run(query, params)
        .then((result) => {
          // console.log('Relaciones encontradas:', result.records);
          this.relaciones = result.records.map(record => {
            return { relation: record.get('r'), relatedNode: record.get('m') };
            });
        })
        .catch((error) => {
          console.error('Error al obtener las relaciones:', error);
        })
        .finally(() => {
          session.close();
        });
    },
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
    addNewProperty() {
      // Añadir un objeto que represente la nueva propiedad con clave y valor vacíos
      this.newProperties.push({ key: '', value: '' });
    },
    deleteTextbox(index) {
      this.newProperties.splice(index, 1); // Elimina el elemento en el índice dado
    },
    saveChanges() {
      const session = getSession();
      const numericId = parseInt(this.id);

      // Comenzar con las propiedades existentes
      let query = 'MATCH (n) WHERE ID(n) = $id SET ';
      let setClauses = Object.keys(this.nodeProperties).map(key => `n.${key} = $${key}`);
      const params = { id: numericId, ...this.nodeProperties };

      // Añadir las nuevas propiedades
      this.newProperties.forEach((prop, index) => {
          if (prop.key && prop.value) { // Asegúrate de que la clave y el valor no están vacíos
          // Agrega una nueva propiedad en la consulta Cypher y en los parámetros
          setClauses.push(`n.${prop.key} = $newPropValue${index}`);
          params[`newPropValue${index}`] = prop.value;
          }
      });

      // Completar la consulta Cypher con todas las cláusulas SET
      query += setClauses.join(', ');

      // Ejecutar la consulta Cypher con los parámetros
      session
          .run(query, params)
          .then(() => {
            if (this.applyToNodes > 0) {
              this.applyChangesToFollowingNodes();
            }
            else {
              // Manejar el caso de éxito
              alert('Nodo actualizado con éxito!');
              this.$router.go(-1); // Reemplaza esto con tu ruta deseada
            }
            
          })
          .catch(error => {
            // Manejar el caso de error
            console.error('Error al guardar los cambios:', error);
          })
          .finally(() => {
            session.close(); // Cerrar la sesión
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
          alert('Nodos actualizados con éxito!');
        })
        .catch(error => {
          console.error('Error al eliminar la propiedad:', error);
        })
        .finally(() => {
          if (this.applyToNodes <= 0) {
            session.close();
          }
        });
    },
    applyChangesToFollowingNodes() {
      const session = getSession();
      const numericId = parseInt(this.id);
      const startId = numericId;
      const endId = startId + this.applyToNodes;
      // Primero, obtenemos las etiquetas del nodo original
      session.run('MATCH (n) WHERE ID(n) = $id RETURN labels(n) as labels', { id: numericId })
        .then(result => {
          if (result.records.length == this.applyToNodes) {
            const originalNodeLabels = result.records[0].get('labels');
            // Ahora aplicamos los cambios a los nodos sucesivos que compartan al menos una etiqueta
            for (let i = 1; i <= this.applyToNodes; i++) {
              let nodeId = startId + i;
              // Verificamos si el nodo sucesivo comparte alguna etiqueta
              session.run(`
                MATCH (n)
                WHERE ID(n) = $nodeId AND any(label IN labels(n) WHERE label IN $originalNodeLabels)
                SET n += $properties
                RETURN n
              `, {
                nodeId: nodeId,
                originalNodeLabels: originalNodeLabels,
                properties: this.nodeProperties
              })
              .then(result => {
                if (result.records.length === 0) {
                  alert('ERROR: Alguno de los nodos a editar no comparte etiquetas con el nodo original.');
                } else {
                  alert(`Nodos actualizados con éxito!`);
                  this.$router.go(-1); // Reemplaza esto con tu ruta deseada
                }
              })
              .catch(error => {
                console.error(`Error al actualizar el nodo con ID ${nodeId}:`, error);
              })
              .finally(() => {
                if (nodeId === endId) {
                  session.close(); // Asegurarnos de cerrar la sesión cuando hayamos terminado con el último nodo
                }
              });
            }
          } else {
            alert('ERROR: Alguno de los nodos a editar no comparte etiquetas con el nodo original.');
            session.close();
          }
        })
        .catch(error => {
          console.error('Error al recuperar las etiquetas del nodo original:', error);
          session.close();
        });
    },
  },
};
</script>

<style>

.edit-container {
  margin-bottom: 1rem;
  width: 98% !important;
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 1rem;
  width: 98% !important;
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

.changes {
  border-collapse: collapse;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 16px;
  /*margin-left: 1%;*/
  font-weight: 900;
  color: #226946;
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
  width: 94% !important;
  margin-left: 1% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.multiple-nodes {
  display: inline-block !important;
  width: 20% !important;
  height: 30px !important;
  margin-left: 1% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.save {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1.5% !important;
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
