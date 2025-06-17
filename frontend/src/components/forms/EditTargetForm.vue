<script>
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import net from '../../services/NetworkService';
import errors from '../../constants/errors';
import ENDPOINTS from '../../constants/endpoints';
import { EventBus } from '../../constants/eventBus';

export default {
  name: "EditTargetForm",
  components: {
    BlankFormLayout,
  },
  props: {
    target: {
      type: Object,
      required: true
    }
  },
  emits: ['target-updated', 'error'],
  data() {
    return {
      targetName: this.target.name,
      updatedTargetUrl: this.target.url,
      loading: false,
    };
  },
  methods: {
    async updateTarget() {
      this.loading = true;

      if (!this.targetName.trim()) {
        errors.value.push({ type: "danger", message: "Target Name cannot be empty." });
        return;
      }

      if (!this.updatedTargetUrl.trim()) {
        errors.value.push({ type: "danger", message: "Website URL cannot be empty." });
        return;
      }

      const urlRegex = /^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})$/i;
      if (!urlRegex.test(this.updatedTargetUrl)) {
        errors.value.push({ type: "danger", message: "Please enter a valid URL (e.g., https://example.com)." });
        return;
      }

      try {
        await net.put(`${ENDPOINTS.TARGET}${this.target.target_id}`, {
          name: this.targetName,
          url: this.updatedTargetUrl,
        });

        errors.value.push({ type: "success", message: `Target "${this.targetName}" updated successfully.` });
        EventBus.emit('refresh-targets');
        this.$emit('target-updated')
      } catch (err) {
        errors.value.push({ type: "danger", message: `Failed to update target.` });
        this.$emit('error', err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div v-if="loading">...</div>
  <div class="card-body">
    <form @submit.prevent="updateTarget">
      <div class="mb-3">
        <label for="targetName" class="form-label">Target Name</label>
        <input
          type="text"
          class="form-control"
          id="targetName"
          v-model="targetName"
          placeholder="e.g., My Website"
          required
        />
      </div>
      <div class="mb-3">
        <label for="targetUrl" class="form-label">Website URL</label>
        <input
          type="url"
          class="form-control"
          id="targetUrl"
          v-model="updatedTargetUrl"
          placeholder="e.g., https://www.google.com"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">
        <i class="bi bi-save me-1"></i> Save Changes
      </button>
    </form>
  </div>
</template>
