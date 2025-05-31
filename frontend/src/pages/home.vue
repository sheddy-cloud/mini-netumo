<script setup>
import { ref, onMounted } from 'vue';
import PanelLayout from '../Layouts/PanelLayout.vue';
import { getTargets, createTarget } from '../services/monitorService'; // Import createTarget

const nodeId = import.meta.env.VITE_NODE_ID;
const targets = ref([]);
const newTargetUrl = ref(''); // State for the new target URL form input
const isLoading = ref(true); // Loading state for fetching targets
const errorMessage = ref(''); // Error message for fetching/adding targets
const successMessage = ref(''); // Success message after adding target

// Function to fetch targets
const fetchTargets = async () => {
    isLoading.value = true;
    errorMessage.value = ''; // Clear previous errors
    try {
        targets.value = await getTargets();
        if (targets.value.length === 0) {
            errorMessage.value = 'No monitoring targets configured. Add one below!';
        }
    } catch (err) {
        console.error("Error loading targets:", err);
        errorMessage.value = 'Failed to load targets. Please ensure the backend is running and accessible.';
        targets.value = []; // Clear targets on error
    } finally {
        isLoading.value = false;
    }
};

// Function to add a new target
const addTarget = async () => {
    if (!newTargetUrl.value.trim()) {
        errorMessage.value = 'Target URL cannot be empty.';
        return;
    }
    // Basic URL validation
    const urlRegex = /^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})$/i;
    if (!urlRegex.test(newTargetUrl.value)) {
        errorMessage.value = 'Please enter a valid URL (e.g., https://example.com).';
        return;
    }

    errorMessage.value = ''; // Clear previous errors
    successMessage.value = ''; // Clear previous success messages

    try {
        // Assuming createTarget returns the new target object
        const createdTarget = await createTarget({ url: newTargetUrl.value });
        targets.value.push(createdTarget); // Add new target to the list
        newTargetUrl.value = ''; // Clear the form input
        successMessage.value = `Target "${createdTarget.url}" added successfully!`;
        // Re-fetch targets to ensure data consistency and potentially get more details if needed
        await fetchTargets();
    } catch (err) {
        console.error("Error adding target:", err);
        errorMessage.value = `Failed to add target: ${err.response?.data?.message || err.message}.`;
    }
};

onMounted(() => {
    fetchTargets(); // Initial fetch on component mount
});
</script>

<template>
    <PanelLayout title="Home" :breadcrumb="['Home', 'Dashboard']">
        <div class="dashboard-container">
            <h1>MIN-NETUMO MONITORING PLATFORM</h1>
            <p>Frontend Node ID: <strong>{{ nodeId }}</strong></p>

            <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
            <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

            <div class="card add-target-card mb-4">
                <div class="card-header">
                    <h4>Add New Monitoring Target</h4>
                </div>
                <div class="card-body">
                    <form @submit.prevent="addTarget">
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

            <div v-if="isLoading" class="text-center my-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading targets...</span>
                </div>
                <p>Loading targets...</p>
            </div>
            <div v-else-if="targets.length > 0" class="targets-grid">
                <div
                    v-for="target in targets"
                    :key="target.id"
                    class="target-card card"
                >
                    <div class="card-body">
                        <h5 class="card-title">{{ target.url }}</h5>
                        <p class="card-text">Status:
                            <span :class="{'text-success': target.status === 'UP', 'text-danger': target.status === 'DOWN'}">
                                <strong>{{ target.status }}</strong>
                            </span>
                        </p>
                        <p class="card-text">Latency: {{ target.latency || 'N/A' }} ms</p>
                        <p class="card-text">SSL expires in: {{ target.ssl_days !== undefined ? target.ssl_days + ' days' : 'N/A' }}</p>
                        <p class="card-text">Domain expires in: {{ target.domain_days !== undefined ? target.domain_days + ' days' : 'N/A' }}</p>
                        </div>
                </div>
            </div>
            <div v-else-if="!isLoading && !errorMessage">
                <p class="text-muted">No targets found. Add a new target using the form above.</p>
            </div>
        </div>
    </PanelLayout>
</template>

<style scoped>
.dashboard-container {
    padding: 20px;
}

.card {
    border: 1px solid #e0e0e0;
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.add-target-card {
    margin-bottom: 2rem;
}

.targets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.target-card .card-body {
    padding: 1.25rem;
}

.target-card .card-title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    word-break: break-all; /* Ensures long URLs wrap */
}

.target-card .card-text {
    margin-bottom: 0.5rem;
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
</style>