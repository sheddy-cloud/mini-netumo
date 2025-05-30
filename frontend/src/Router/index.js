import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../Views/Dashboard.vue'
import LoginPage from '../Views/LoginPage.vue' // 👈 import it

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/login', // 👈 define this route
    name: 'Login',
    component: LoginPage
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
