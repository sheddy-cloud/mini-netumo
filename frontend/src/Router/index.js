import { createRouter, createWebHistory } from 'vue-router'
import login from "../pages/login.vue"

const routes = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/login',
    name: 'login',
    component: login
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
