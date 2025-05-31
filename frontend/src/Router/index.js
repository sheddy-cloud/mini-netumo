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
    // Added: The registration page path
    path: '/register',
    name: 'Register', // Unique name for the register route
    component: RegisterPage, // Link to your RegisterPage component
    meta: {
      title: 'Register for Netumo' // Page title for the registration page
    }
  },
  {
    // This is the root path, currently set to your Dashboard
    path: '/',
    name: 'Dashboard', // Name for the dashboard route
    component: Home,
    meta: {
      title: 'Netumo Dashboard', // Page title for the dashboard
      // You might add meta: { requiresAuth: true } here later for authentication
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

// Global navigation guard to update page titles based on route meta
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Netumo Lite'; // Default title if not specified
  next();
});


router.afterEach((to, from) => {
  document.body.classList.remove('toggle-sidebar')
})

export default router
