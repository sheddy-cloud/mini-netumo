<script>
import PanelLayout from '../Layouts/PanelLayout.vue';
import AddTargetForm from '../components/forms/AddTargetForm.vue'; // Import the AddTargetForm component
import { getTargets } from '../services/monitorService'; // Only need getTargets here

export default {
    name: "HomePage",
    components: {
        PanelLayout,
        AddTargetForm // Register the AddTargetForm component
    },
    data() {
        return {
            // nodeId: import.meta.env.VITE_NODE_ID, // Removed as requested
            targets: [],
            isLoading: true, // Loading state for fetching targets
            homePageErrorMessage: '', // Use a distinct name for Home page errors
            homePageSuccessMessage: '', // Use a distinct name for Home page success
        };
    },
    mounted() {
        this.fetchTargets(); // Initial fetch on component mount
    },
    methods: {
        // Function to fetch targets
        async fetchTargets() {
            this.isLoading = true;
            this.homePageErrorMessage = ''; // Clear previous errors
            this.homePageSuccessMessage = ''; // Clear previous success messages
            try {
                this.targets = await getTargets();
                if (this.targets.length === 0) {
                    this.homePageErrorMessage = 'No monitoring targets configured.';
                }
            } catch (err) {
                console.error("Error loading targets:", err);
                this.homePageErrorMessage = 'Failed to load targets. Please ensure the backend is running and accessible.';
                this.targets = []; // Clear targets on error
            } finally {
                this.isLoading = false;
            }
        },
        // Handler for when a target is successfully added via the form component
        handleTargetAdded(newTarget) {
            // Re-fetch targets to ensure data consistency and potentially get more details if needed
            this.fetchTargets();
            this.homePageSuccessMessage = `Target "${newTarget.name}" added successfully!`; // Updated message to use target.name
            // Optionally clear success message after a few seconds
            setTimeout(() => { this.homePageSuccessMessage = ''; }, 5000);
        },
        // Handler for errors from the form component
        handleFormError(errorMsg) {
            this.homePageErrorMessage = errorMsg;
            // Optionally clear error message after a few seconds
            setTimeout(() => { this.homePageErrorMessage = ''; }, 5000);
        },
    },
};
</script>

<template>
    <PanelLayout title="Home" :breadcrumb="['Home', 'Dashboard']">
        <div class="dashboard-container">
            <h1>Netumo Lite Dashboard</h1>
            <div v-if="homePageSuccessMessage" class="alert alert-success">{{ homePageSuccessMessage }}</div>
            <div v-if="homePageErrorMessage" class="alert alert-danger">{{ homePageErrorMessage }}</div>

            <AddTargetForm
                @target-added="handleTargetAdded"
                @error="handleFormError"
                class="mb-4"
            />

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
                        <h5 class="card-title">{{ target.name }}</h5> <p class="card-text text-muted">{{ target.url }}</p> <p class="card-text">Status:
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
            <div v-else-if="!isLoading && !homePageErrorMessage && targets.length === 0">
                 <p class="text-muted">No targets found. Use the form above to add your first monitoring target.</p>
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
    margin-bottom: 0.25rem; /* Reduced margin for name */
    word-break: break-all; /* Ensures long names/URLs wrap */
}
.target-card .card-text.text-muted {
    font-size: 0.9rem;
    margin-bottom: 0.75rem; /* Space after URL */
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
