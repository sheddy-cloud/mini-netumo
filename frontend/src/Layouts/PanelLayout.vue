<script>
import { watch } from 'vue';
import PanelHeader from '../components/ui/PanelHeader.vue';
import PanelSidebar from '../components/ui/PanelSidebar.vue';
import Alert from '../components/ui/Alert.vue';
import errors from '../constants/errors.js';

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
      sharedErrors: errors
    };
  },
  watch: {
    title(newTitle) {
      document.title = newTitle;
    }
  },
  created() {
    document.title = this.title;
  },
  methods: {
    removeError(index) {
      this.sharedErrors.splice(index, 1);
    }
  }
}
</script>

<template>
  <PanelHeader />
  <PanelSidebar />
  <main id="main" class="main">
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

    <section class="section dashboard">
      <div class="message position-fixed bottom-0 z-3 p-3" style="z-index: 1000; max-width: 250; right: 0;">
        <Alert v-for="(error, index) in sharedErrors" :key="index" :type="error.type" :message="error.message"
          @close="removeError(index)" />
      </div>
      <slot />
    </section>
  </main>
</template>
