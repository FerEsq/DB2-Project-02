<template>
  <div id="app">
    <nav>
    <router-link to="/crear" class="noneDec"> 
      <div class="nav-brand">
        <img src="@/assets/icon.png" alt="Logo" class="logo"/> 
        <span class="brand-text">UVG Connect</span>
      </div>
    </router-link>
      <div class="nav-items">
        <router-link to="/crear" class="nav-item">Crear nodo</router-link>
        <router-link to="/gestionarRelaciones" class="nav-item">Gestionar Relaciones</router-link>
        <router-link to="/usuario" class="nav-item">Usuarios</router-link>
        <router-link to="/curso" class="nav-item">Cursos</router-link>
        <router-link to="/evento" class="nav-item">Eventos</router-link>
        <router-link to="/facultad" class="nav-item">Facultades</router-link>
        <router-link to="/salon" class="nav-item">Salones</router-link>
        <router-link to="/club" class="nav-item">Clubes</router-link>
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
  color: white !important;
}

.nav-brand .brand-text {
  text-decoration: none !important;
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

.noneDec {
  text-decoration: none !important;
}

</style>
