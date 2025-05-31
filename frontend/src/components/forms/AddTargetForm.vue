<script>
// Adjust path to BlankFormLayout based on its actual location relative to components/forms
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import { createTarget } from '../../services/monitorService'; // Import createTarget

export default {
    name: "AddTargetForm",
    components: {
        BlankFormLayout, // Register BlankFormLayout if used
    },
    // Define the events this component can emit
    emits: ['target-added', 'error'],
    data() {
        return {
            targetName: '',    // New state for the target name input
            newTargetUrl: '',  // Existing state for the website URL input
            formErrorMessage: '', // Error message for adding targets
            formSuccessMessage: '', // Success message after adding target
        };
    },
    methods: {
        // Function to add a new target
        async addTarget() {
            this.formErrorMessage = ''; // Clear previous errors
            this.formSuccessMessage = ''; // Clear previous success messages

            // Validation for both name and URL
            if (!this.targetName.trim()) {
                this.formErrorMessage = 'Target Name cannot be empty.';
                return;
            }
            if (!this.newTargetUrl.trim()) {
                this.formErrorMessage = 'Website URL cannot be empty.';
                return;
            }

            // Basic URL validation
            const urlRegex = /^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})$/i;
            if (!urlRegex.test(this.newTargetUrl)) {
                this.formErrorMessage = 'Please enter a valid URL (e.g., https://example.com).';
                return;
            }

            try {
                // Assuming createTarget returns the new target object
                // Send both name and url to the backend
                const createdTarget = await createTarget({
                    name: this.targetName,
                    url: this.newTargetUrl
                });

                this.targetName = '';    // Clear the name input
                this.newTargetUrl = ''; // Clear the URL input
                this.formSuccessMessage = `Target "${createdTarget.name}" added successfully!`;
                // Emit an event to the parent component (Home.vue) to notify about the new target
                this.$emit('target-added', createdTarget);
            } catch (err) {
                console.error("Error adding target from form:", err);
                const backendMessage = err.response?.data?.message || err.message;
                this.formErrorMessage = `Failed to add target: ${backendMessage}.`;
                // Emit an error event if the parent needs to handle it globally
                this.$emit('error', this.formErrorMessage);
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
        <div class="card-body">
            <div v-if="formSuccessMessage" class="alert alert-success">{{ formSuccessMessage }}</div>
            <div v-if="formErrorMessage" class="alert alert-danger">{{ formErrorMessage }}</div>

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

<style scoped>
.add-target-form-component {
    border: 1px solid #e0e0e0;
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
    padding: 1rem 1.25rem;
    border-top-left-radius: calc(0.5rem - 1px);
    border-top-right-radius: calc(0.5rem - 1px);
}
.card-body {
    padding: 1.25rem;
}
.alert {
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
}
.alert-success {
    color: #0f5132;
    background-color: #d1e7dd;
    border-color: #badbcc;
}
.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}
.form-label {
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: block;
}
.form-control {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.form-control:focus {
    color: #495057;
    background-color: #fff;
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
    color: white;
    padding: 0.75rem 1.25rem;
    font-size: 1.1rem;
    border-radius: 0.3rem;
    transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}
.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}
</style>
