<script>
// Adjust path to BlankFormLayout based on its actual location relative to components/forms
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import net from '../../services/NetworkService';
import errors from '../../constants/errors';
import ENDPOINTS from '../../constants/endpoints';
import { EventBus } from '../../constants/eventBus';

export default {
    name: "AddTargetForm",
    components: {
        BlankFormLayout,
    },
    emits: ['target-added', 'error'],
    data() {
        return {
            targetName: '',
            newTargetUrl: '',
            loading: false,
        };
    },
    methods: {
        // Function to add a new target
        async addTarget() {
            this.loading = true
            // Validation for both name and URL
            if (!this.targetName.trim()) {
                errors.value.push({type: "danger", message: "Target Name cannot be empty."})
                return;
            }
            if (!this.newTargetUrl.trim()) {
                errors.value.push({type: "danger", message: "Website URL cannot be empty."})
                return;
            }

            // Basic URL validation
            const urlRegex = /^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})$/i;
            if (!urlRegex.test(this.newTargetUrl)) {
                errors.value.push({type: "danger", message: "Please enter a valid URL (e.g., https://example.com)."})
                return;
            }

            try {
                const createdTarget = await net.post(ENDPOINTS.TARGET, {
                    name: this.targetName,
                    url: this.newTargetUrl
                });

                this.targetName = '';
                this.newTargetUrl = '';
                errors.value.push({type: "success", message: `Target "${createdTarget.data.name}" added successfully!`})
                EventBus.emit('refresh-sidebar')
            } catch (err) {
                errors.value.push({type: "danger", message: `An error occured while submitting the form`})
            }finally{
                this.loading = false
            }
        },
    },
};
</script>

<template>
    <div class="card add-target-form-component">
        <div class="card-header">
            <h4>Add New Monitoring Target</h4>
        </div>
        <div v-if="loading">...</div>
        <div class="card-body">
            <form @submit.prevent="addTarget">
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
                        v-model="newTargetUrl"
                        placeholder="e.g., https://www.google.com"
                        required
                    />
                </div>
                <button type="submit" class="btn btn-primary">Add Target</button>
            </form>
        </div>
    </div>
</template>
