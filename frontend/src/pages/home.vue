<script>
import PanelLayout from '../Layouts/PanelLayout.vue';
import AddTargetForm from '../components/forms/AddTargetForm.vue';
import Card from '../components/ui/Card.vue';
import GeneralLatecyChart from '../components/ui/GeneralLatecyChart.vue';
import TargetsTable from '../components/ui/TargetsTable.vue';

export default {
    name: "HomePage",
    components: {
        PanelLayout,
        AddTargetForm,
        GeneralLatecyChart,
        Card,
        TargetsTable
    },
};
</script>

<template>
    <PanelLayout title="Home" :breadcrumb="['Home', 'Dashboard']">
        <div class="row g-3 mb-4">
            <div>
                <Card title="Latecy Report">
                    <GeneralLatecyChart />
                </Card>
            </div>
            <div class="col-md-7">
                <Card title="Websites">
                    <TargetsTable />
                </Card>
            </div>
            <div class="col-md-5">
                <Card title="Add New Monitoring Target">
                    <AddTargetForm/>
                </Card>
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
    margin-bottom: 0.25rem;
    word-break: break-all;
}

.target-card .card-text.text-muted {
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
    /* Space after URL */
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
