<template>
  <div id="app">
    <nav>
      <div class="nav-brand">
        <img src="@/assets/icon.png" alt="Logo" class="logo"/> <!-- Asegúrate de que la ruta al archivo de imagen sea correcta -->
        UVG Connect
      </div>
      <div class="nav-items">
        <router-link to="/usuario" class="nav-item">Usuario</router-link>
        <router-link to="/curso" class="nav-item">Curso</router-link>
        <router-link to="/evento" class="nav-item">Evento</router-link>
        <router-link to="/facultad" class="nav-item">Facultad</router-link>
        <router-link to="/salon" class="nav-item">Salón</router-link>
        <router-link to="/club" class="nav-item">Club</router-link>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Verdana, Geneva, sans-serif;
}

.logo {
  height: 60px; /* Ajusta esto según el tamaño deseado */
  margin-right: 10px; /* Añade un poco de margen a la derecha de la imagen */
  margin-top: 5px;
  margin-bottom: 5px;
  vertical-align: middle; /* Alinea verticalmente la imagen con el texto */
}

nav {
  background-color: #226946;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
}

.nav-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-items {
  display: flex;
}

.nav-item {
  text-decoration: none;
  margin-left: 1rem;
  color: white;
  transition: color 0.3s ease;
}

.nav-item:hover, .router-link-exact-active {
  color: #BEDCFE;
}
</style>
