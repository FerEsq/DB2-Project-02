<template>
  <div>
    <h1 class="title">Crear Nodo</h1>
    <div>
      <form @submit.prevent="createNode">
          <div class="labels-group">
            <p class="select">Seleccionar Label(s):</p>
            <div v-for="label in labels" :key="label">
              <input
                type="checkbox"
                :id="`label-${label}`"
                :value="label"
                v-model="selectedLabels"
              />
              <label :for="`label-${label}`">{{ label }}</label>
            </div>
          </div>
          <!-- Estos son los textbox con la propiedad obligatoria -->
          <div>
            <input
                type="text"
                placeholder="Nombre de la propiedad"
                v-model="requiredPropertyName"
                class="form-control"
            />
            <p class="obligatorio"> * </p>
            <input
                type="text"
                placeholder="Valor de la propiedad"
                v-model="requiredPropertyValue"
                class="form-control"
            />
            <p class="obligatorio"> * </p>
          </div>

            <div v-for="(property, index) in newProperties" :key="index" class="form-group new-property">
            <!-- Estos son los textbox que se agregan para las demas propiedades opcionales -->
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
        <button type="submit" class="save">Crear</button>
      </form>
    </div>
  </div>
</template>

<script>
import { getSession } from '../Neo4j'; // Asegúrate de que este sea el camino correcto para tu configuración

export default {
  name: 'CrearNodo',
  props: {
    id: {
      type: Number, // O String, dependiendo del tipo de dato que sea el ID
      required: true
    }
  },
  data() {
    return {
      requiredPropertyName: '',
      requiredPropertyValue: '',
      labels: [],
      selectedLabels: [],
      newProperties: [],
    };
  },
  created() {
    this.fetchLabels();
  },
  methods: {
    fetchLabels() {
      const session = getSession();
      session
        .run('CALL db.labels()')
        .then(result => {
          this.labels = result.records.map(record => record.get('label'));
          // Establecer una label por defecto si es necesario
          this.selectedLabels = [this.labels[0]]; // Por ejemplo, selecciona la primera label por defecto
        })
        .catch(error => {
          console.error('Error al buscar las labels:', error);
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
    createNode() {
      if (!this.requiredPropertyName.trim() || !this.requiredPropertyValue.trim()) {
        alert('Por favor, llene la propiedad y el valor obligatorios.');
        return;
      }

      if (this.selectedLabels.length === 0) {
        alert('Debe seleccionar al menos una label.');
        return;
      }

      const session = getSession();
      let propertiesObject = {
        [this.requiredPropertyName.trim()]: this.requiredPropertyValue.trim()
      };
      this.newProperties.forEach((prop) => {
        if (prop.key.trim() && prop.value.trim()) {
          propertiesObject[prop.key.trim()] = prop.value.trim();
        }
      });

      const labelsString = this.selectedLabels.join(':');
      const query = `CREATE (n:${labelsString} $properties) RETURN n`;
      const params = {
        properties: propertiesObject
      };

      session.run(query, params)
        .then((result) => {
          if (result.records.length > 0) {
            const createdNode = result.records[0].get('n');
            console.log('Nodo creado con éxito:', createdNode);
            alert('Nodo creado con éxito!');
            //this.$router.push('/usuario'); // Reemplaza con tu ruta deseada
          } else {
            alert('No se pudo crear el nodo.');
          }
        })
        .catch((error) => {
          console.error('Error al crear el nodo:', error);
          alert('Hubo un error al crear el nodo.');
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

input[type="checkbox"] {
  margin-right: 5px; 
  color: #226946 !important;
}

.select {
  font-family: Verdana, Geneva, sans-serif;
  font-size: 20px;
  font-weight: bold;
  color: #226946 !important;
  margin-bottom: -0.5px;
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
  width: 94% !important;
  margin-left: 1% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.labels-group {
  margin-left: 1% !important;
  margin: 1rem 0;
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

.obligatorio {
  display: inline-block !important;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 20px;
  font-weight: bold;
  margin-left: 1%;
  color: #D52941!important;
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
