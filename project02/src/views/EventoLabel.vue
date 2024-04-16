<template>
  <div>
    <h1 class="title">Eventos</h1>
    <input
      v-model="searchQuery"
      @input="filterNodes"
      placeholder="Buscar..."
      type="text"
      class="search-input"
    />
    <button class="add" @click="deleteMultiplesNodes">Eliminar rango de nodos</button>
    <select v-model="startNode" id="startNode" class="select-nodes">
      <option v-for="id in userIDs" :key="id" :value="id">{{ id }}</option>
    </select>
    <select v-model="endNode" id="endNode" class="select-nodes">
      <option v-for="id in userIDs" :key="id" :value="id">{{ id }}</option>
    </select>
    <table class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titulo</th>
          <th>Descripcion</th>
          <th>Fecha de Inicio</th>
          <th>Fecha de Fin</th>
          <th>Participantes</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.titulo }}</td>
          <td>{{ user.descripcion }}</td>
          <td>{{ user.fechaInicio }}</td>
          <td>{{ user.fechaFin }}</td>
          <td>{{ user.participantes }}</td>
          <td>
            <button class="btn btn-delete" @click="deleteUser(user.id)">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff">
                <path d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="btn btn-edit" @click="editUser(user)">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 8.00012L4 16.0001V20.0001L8 20.0001L16 12.0001M12 8.00012L14.8686 5.13146L14.8704 5.12976C15.2652 4.73488 15.463 4.53709 15.691 4.46301C15.8919 4.39775 16.1082 4.39775 16.3091 4.46301C16.5369 4.53704 16.7345 4.7346 17.1288 5.12892L18.8686 6.86872C19.2646 7.26474 19.4627 7.46284 19.5369 7.69117C19.6022 7.89201 19.6021 8.10835 19.5369 8.3092C19.4628 8.53736 19.265 8.73516 18.8695 9.13061L18.8686 9.13146L16 12.0001M12 8.00012L16 12.0001" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// Asumiendo que has creado un archivo db.js como se mostró anteriormente
import { getSession } from '../Neo4j.js';

export default {
  name: 'EventoLabel',
  data() {
    return {
      searchQuery: '',
      users: [],
      startNode: null,
      endNode: null,
      usersIDs: [],
    }
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
    const session = getSession();
    return session
      .run('MATCH (u:Evento) RETURN u, ID(u) as id')
      .then(result => {
        this.userIDs = result.records.map(record => record.get('id').toNumber());
        this.users = result.records.map(record => {
          return {
            id: record.get('id').toNumber(), // Convertir a número si es un Integer de Neo4j
            titulo: record.get('u').properties.titulo,
            descripcion: record.get('u').properties.descripcion,
            fechaInicio: record.get('u').properties.fechaInicio,
            fechaFin: record.get('u').properties.fechaFin,
            participantes: record.get('u').properties.participantes
            // ... otras propiedades que quieras incluir
          };
        });
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        session.close();
      });
  },
    filterNodes() {
      this.fetchUsers().then(() => {
        if (this.searchQuery) {
          this.users = this.users.filter((user) => {
            return Object.values(user).some(
              // Solo convierte en string si el valor no es undefined
              (prop) => prop !== undefined && prop.toString().includes(this.searchQuery)
            );
          });
        }
      });
    },
    deleteUser(userId) {
      const session = getSession();

      // Iniciar una transacción para manejar la eliminación de relaciones y el nodo
      session.writeTransaction((tx) => {
        // Primero eliminar todas las relaciones del nodo
        tx.run('MATCH (u:Facultad)-[r]-() WHERE ID(u) = $userId DELETE r', { userId: parseInt(userId) });
        
        // Luego eliminar el nodo
        return tx.run('MATCH (u:Facultad) WHERE ID(u) = $userId DELETE u', { userId: parseInt(userId) });
      })
      .then(() => {
        // Actualizar la lista de usuarios en la interfaz de usuario
        this.users = this.users.filter(user => user.id !== userId);
        // Notificar al usuario de la eliminación exitosa
      })
      .catch(error => {
        console.error('Error al eliminar el nodo:', error);
        // Manejar errores, por ejemplo, mostrando un mensaje al usuario
      })
      .finally(() => {
        // Cerrar la sesión de Neo4j
        session.close();
      });
    },
    editUser(user) {
      //Usar this.$router.push para pasar todo el objeto user como parámetro de estado
      this.$router.push({ name: 'EditarNodo', params: { id: user.id } });
    },
    navigateToAddUser() {
      this.$router.push('/crear');
    },
    deleteMultiplesNodes() {
      const session = getSession();
      const startNode = this.startNode;
      const endNode = this.endNode;

      if (startNode == null || endNode == null || startNode > endNode) {
        alert('Rango de IDs no válido.');
        return;
      }

      let deleteQuery = `
        MATCH (n)
        WHERE ID(n) >= $startNode AND ID(n) <= $endNode
        DETACH DELETE n
      `;

      session.run(deleteQuery, { startNode, endNode })
        .then(() => {
          alert('Nodos eliminados con éxito!');
          //Reflejar que los nodos han sido eliminados
          this.fetchUsers();
        })
        .catch(error => {
          console.error('Error al eliminar nodos:', error);
          alert('Error al eliminar nodos. Verifique que no tengan relaciones.');
        })
        .finally(() => {
          session.close();
        });
    },
  },
}
</script>

<style>
.title {
  border-collapse: collapse;
  margin-top: 1rem;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 30px;
  margin-left: 1%;
  font-weight: bold;
  color: #226946;
}

.add {
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
}

.search-input {
  width: 61% !important;
  margin-left: 1% !important;
  padding: 0.5rem;
  margin: 1rem 0;
  border: 2px solid #226946;
  border-radius: 4px;
}

.select-nodes {
  display: inline-block !important;
  width: 8% !important;
  height: 44.5px !important;
  margin-left: 1% !important;
  margin: 1rem 0;
  border: 2px solid #226946 !important;
  border-radius: 4px;
}

.user-table {
  width: 98%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-family: Verdana, Geneva, sans-serif;
  font-size: 15px;
  margin-left: 1%;
}

.user-table th,
.user-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.user-table th {
  background-color: #226946;
  color: white;
}

.user-table tbody tr:nth-child(odd) {
  background-color: #f2f2f2;
}

.user-table tbody tr:hover {
  background-color: #ddd;
}

.btn {
  padding: 5px 10px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete {
  background-color: #D52941 !important;
  color: white !important;
}

.btn-edit {
  background-color: #266DD3 !important;
  color: white !important;
}

.btn svg {
  height: 1em; /* O el tamaño que prefieras */
  width: 1em; /* Mantén la misma altura y ancho para preservar la proporción */
}

</style>