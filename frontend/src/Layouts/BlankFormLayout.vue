<script>
import Alert from '../components/ui/Alert.vue';
import errors from '../constants/errors.js';

export default {
  name: 'BlankFormLayout',
  components: {
    Alert,
  },
  data() {
    return {
      sharedErrors: errors
    };
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
  <main>
    <div class="container">

      <section class="section register min-vh-100 d-flex flex-column align-items-center justify-content-center py-4">
        <div class="container">
          <div class="message p-3" style="max-width: 250;">
            <Alert v-for="(error, index) in sharedErrors" :key="index" :type="error.type" :message="error.message"
              @close="removeError(index)" />
          </div>
          <slot />
        </div>
      </section>
    </div>
  </main>
</template>
