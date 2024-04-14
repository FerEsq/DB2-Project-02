import { createRouter, createWebHistory } from 'vue-router';
import UsuarioLabel from '../views/UsuarioLabel.vue';
import CursoLabel from '../views/CursoLabel.vue';
import EventoLabel from '../views/EventoLabel.vue';
import FacultadLabel from '../views/FacultadLabel.vue';
import SalonLabel from '../views/SalonLabel.vue';
import ClubLabel from '../views/ClubLabel.vue';
import EditarNodo from '../views/EditarNodo.vue';
import CrearNodo from '../views/CrearNodo.vue';

const routes = [
  { path: '/', redirect: '/crear' },
  { path: '/crear', component: CrearNodo },
  { path: '/usuario', component: UsuarioLabel },
  { path: '/curso', component: CursoLabel },
  { path: '/evento', component: EventoLabel },
  { path: '/facultad', component: FacultadLabel },
  { path: '/salon', component: SalonLabel },
  { path: '/club', component: ClubLabel },
  {path: '/editar/:id', name: 'EditarNodo', component: EditarNodo, props: true
  }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
