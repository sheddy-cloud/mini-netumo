<script>
import PanelLayout from '../../Layouts/PanelLayout.vue';
import net from '../../services/NetworkService';
import ENDPOINTS from '../../constants/endpoints';

export default {
    name: "target_details",
    props: ['id'],
    data() {
        return {
            loading: true,
            error: "",
            target: {},
        }
    },
    methods: {
        async fetchTarget() {
            try {
                const res = await net.get(`${ENDPOINTS.TARGET}${this.id}`)
                this.target = res.data
            } catch (e) {
                this.error = "Failed to get detail for this website"
            } finally {
                this.loading = false
            }
        }
    },
    created() {
        this.fetchTarget()
    },
    components: {
        PanelLayout
    },
    watch: {
        id(newId, oldId) {
            if (newId !== oldId) {
                this.fetchTarget()
            }
        }
    },
}
</script>

<template>
    <PanelLayout :title="target.name || '...'" :breadcrumb="['Websites', target.name || '...']">
        <div v-if="loading">Loading target details...</div>
        <div v-else>
            <h1>{{ target.name }}</h1>
        </div>
    </PanelLayout>
</template>
