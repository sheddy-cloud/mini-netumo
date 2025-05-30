import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../Views/Dashboard.vue'
import LoginPage from '../Views/LoginPage.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
