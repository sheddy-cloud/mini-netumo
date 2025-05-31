// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your page components
import Login from "../pages/login.vue"; // Renamed import to 'Login' for clarity
import Home from "../pages/home.vue";   // Renamed import to 'Home' for clarity
import Error404 from "../pages/error404.vue";

const routes = [
  {
    // This is now the root path, making your Dashboard the first page
    path: '/',
    name: 'Dashboard', // Changed name to 'Dashboard' for clarity
    component: Home,
    meta: {
      title: 'Netumo Dashboard' // Page title for the dashboard
    }
  },
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
    // Catch-all route for 404 errors
    // This regex matches any path and captures it, making it a wildcard route.
    // It should ALWAYS be the last route in your configuration.
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: Error404,
    meta: {
      title: 'Page Not Found' // Page title for 404
    }
  }
  // Add other routes here as your application grows, e.g.,
  // {
  //   path: '/settings',
  //   name: 'Settings',
  //   component: () => import('../pages/Settings.vue'), // Example of lazy loading
  //   meta: { requiresAuth: true, title: 'Settings' } // Example meta for auth
  // }
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
