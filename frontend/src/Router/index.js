import { createRouter, createWebHistory } from 'vue-router'
import login from "../pages/login.vue"
import home from "../pages/home.vue"
import error404 from "../pages/error404.vue"

const routes = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/home',
    name: 'home',
    component: home
  },
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: error404
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
