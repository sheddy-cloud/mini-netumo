<script>
import PanelLayout from '../Layouts/PanelLayout.vue';
import AddTargetForm from '../components/forms/AddTargetForm.vue'; // Import the AddTargetForm component

export default {
    name: "HomePage",
    components: {
        PanelLayout,
        AddTargetForm // Register the AddTargetForm component
    },
};
</script>

<template>
    <PanelLayout title="Home" :breadcrumb="['Home', 'Dashboard']">
            <AddTargetForm
                @target-added="handleTargetAdded"
                @error="handleFormError"
                class="mb-4"
            />
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
