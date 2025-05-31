// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your page components
import Home from "../pages/home.vue";
import Login from "../pages/login.vue";
import RegisterPage from "../pages/register.vue"; // Added: Import the RegisterPage component
import Error404 from "../pages/error404.vue";

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
    // Catch-all route for 404 errors
    // This should ALWAYS be the last route in your configuration.
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

export default router;