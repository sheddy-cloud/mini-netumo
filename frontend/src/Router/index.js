import { createRouter, createWebHistory } from 'vue-router'
import login from '../pages/login.vue'
import home from '../pages/home.vue'
import error404 from '../pages/error404.vue'
import register from '../pages/register.vue'
import details from '../pages/targets/details.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: login,
    meta: {
      title: 'Login to Netumo'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: register,
    meta: {
      title: 'Register for Netumo'
    }
  },
  {

    path: '/',
    name: 'Dashboard',
    component: home,
    meta: {
      title: 'Netumo Dashboard'
    }
  },
  {
    path: '/targets/:id',
    name: 'target_details',
    component: details,
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: error404,
    meta: {
      title: 'Page Not Found'
    }
  }
]

const router = createRouter({
  history: createWebHistory(), // Use HTML5 History API for clean URLs
  routes // Your defined routes
})

// Global navigation guard to update page titles based on route meta
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Netumo Lite' // Default title if not specified
  next()
})

router.afterEach((to, from) => {
  document.body.classList.remove('toggle-sidebar')
})

export default router
