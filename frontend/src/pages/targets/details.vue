<script>
import PanelLayout from '../../Layouts/PanelLayout.vue';
import net from '../../services/NetworkService';
import ENDPOINTS from '../../constants/endpoints';
import Card from "../../components/ui/Card.vue"

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
        PanelLayout,
        Card
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


        <div style="display: flex; gap: 1.5rem; width: 100%; margin-right: 0.75rem;" >
            <Card title="Uptime" style="flex: 1;">
                <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-currency-dollar"></i>
                    </div>
                    <div class="ps-3">
                      <h6>90%</h6>
                      <span class="text-success small pt-1 fw-bold">8%</span> <span class="text-muted small pt-2 ps-1">increase</span>
                    </div>
                  </div>
            </Card>
            <Card title="SLL" style="flex: 1;">
                                <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-currency-dollar"></i>
                    </div>
                    <div class="ps-3">
                      <h6>10 Days left</h6>
                      <span class="text-success small pt-1 fw-bold">8%</span> <span class="text-muted small pt-2 ps-1">increase</span>
                    </div>
                  </div>

            </Card>
            <Card title="Registration" style="flex: 1;">
                                <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-currency-dollar"></i>
                    </div>
                    <div class="ps-3">
                      <h6>132 days left</h6>
                      <span class="text-success small pt-1 fw-bold">8%</span> <span class="text-muted small pt-2 ps-1">increase</span>
                    </div>
                  </div>

            </Card>
        </div>
        <div style="display: flex; gap: 1.5rem; width: 100%; margin-right: 0.75rem;" >
            <Card title="Stats" style="flex: 2;">

            </Card>
            <Card title="Alerts" style="flex: 1;">

            </Card>
        </div>
    </PanelLayout>
</template>
