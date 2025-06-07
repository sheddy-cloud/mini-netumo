<script>
import { watch } from 'vue';
import PanelHeader from '../components/ui/PanelHeader.vue';
import PanelSidebar from '../components/ui/PanelSidebar.vue';
import Alert from '../components/ui/Alert.vue';
import errors from '../constants/errors.js';
import { isAuthenticated } from '../services/AuthenticationService.js';
import { EventBus } from '../constants/eventBus.js';

export default {
  name: 'PanelLayout',
  components: {
    PanelHeader,
    PanelSidebar,
    Alert,
  },
  props: {
    title: {
      type: String,
      required: true
    },
    breadcrumb: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      sharedErrors: errors,
      loadingAuth: true,
      refresher: null,
      nodeId: null
    };
  },
  watch: {
    title(newTitle) {
      document.title = newTitle;
    }
  },
  created() {
    document.title = this.title;
    this.checkAuthentication();


    // Fetch the HEAD of the page to get the X-Node-ID from the response headers
    fetch('/', { method: 'HEAD' })
      .then(res => {
        const nodeId = res.headers.get('X-Node-ID');
        if (nodeId) {
          this.nodeId = nodeId;
        }
      })
      .catch(err => {
        console.error('Failed to fetch node ID:', err);
      });
  },
  destroyed(){
    clearInterval(this.refresher);
  },
  methods: {
    removeError(index) {
      this.sharedErrors.splice(index, 1);
    },
    async checkAuthentication() {
      try {
        // Replace this with your actual auth check
        const loggedIn = await isAuthenticated();

        if (!loggedIn) {
          // Redirect to login page if not authenticated
          this.$router.push({ name: 'Login' });
          return;
        }
        this.refresher = setInterval(() => {
          EventBus.emit('refresh-targets')
        }, 10000)

      } catch (error) {
        this.sharedErrors.push({ type: 'danger', message: 'Authentication check failed' });
      } finally {
        this.loadingAuth = false;
      }
    },
  }
}
</script>

<template>
  <PanelHeader />
  <PanelSidebar />
  <main id="main" class="main">
    <div v-if="loadingAuth" class="loading-spinner" style="text-align:center; padding: 2rem;">
      Loading authentication...
      <!-- Node ID display -->
      <div>
        <div v-if="nodeId" class="server-node">
          Served by: {{ nodeId }}
        </div>

      </div>
      <div class="pagetitle">
        <h1>{{ title }}</h1>
        <nav>
          <ol class="breadcrumb">
            <li v-for="(item, index) in breadcrumb" :key="index" class="breadcrumb-item"
              :class="{ active: index === breadcrumb.length - 1 }">
              <a v-if="index !== breadcrumb.length - 1" href="#">{{ item }}</a>
              <span v-else>{{ item }}</span>
            </li>
          </ol>
        </nav>
      </div>
    </div>

    <div v-else>
      <section class="section dashboard">
        <div class="message position-fixed bottom-0 z-3 p-3" style="z-index: 1000; max-width: 250px; right: 0;">
          <Alert v-for="(error, index) in sharedErrors" :key="index" :type="error.type" :message="error.message"
            @close="removeError(index)" />
        </div>
        <slot />
      </section>
    </div>
  </main>


</template>

<style scoped>
.server-node {
  position: fixed;
  bottom: 0;
  right: 0;
  padding: 0.5rem 1rem;
  margin: 1rem;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  z-index: 1200;
}
</style>
