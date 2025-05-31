import { createRouter, createWebHistory } from 'vue-router'
import login from "../pages/login.vue"
import home from "../pages/home.vue"
import error404 from "../pages/error404.vue"
import details from '../pages/targets/details.vue'

const routes = [
  {
    // The explicit login page path
    path: '/login',
    name: 'Login', // Unique name for the login route
    component: Login,
    meta: {
      title: 'Login to Netumo' // Page title for the login page
    }
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
    component: Error404,
    meta: {
      title: 'Page Not Found' // Page title for 404
    }
  }
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(), // Use HTML5 History API for clean URLs
  routes, // Your defined routes
});

router.afterEach((to, from) => {
  document.body.classList.remove('toggle-sidebar')
})

export default router
