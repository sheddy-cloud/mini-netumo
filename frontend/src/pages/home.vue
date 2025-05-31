<style>
</style>

<script>
import PanelLayout from '../Layouts/PanelLayout.vue'

export default {
    name: "home",
    components: {
        PanelLayout,
    }
}
</script>

<template>
    <PanelLayout title="Home" :breadcrumb="['Home', 'Dashboard']">
        <h1>Home</h1>
    </PanelLayout>
</template>
