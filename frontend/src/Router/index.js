import { createRouter, createWebHistory } from 'vue-router'
import login from "../pages/login.vue"
import home from "../pages/home.vue"
import error404 from "../pages/error404.vue"
import details from '../pages/targets/details.vue'

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
    path: "/targets/:id",
    name: "target_details",
    component: details,
    props: true
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

router.afterEach((to, from) => {
  document.body.classList.remove('toggle-sidebar')
})

export default router
