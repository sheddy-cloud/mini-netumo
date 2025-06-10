<script>
import ApexCharts from 'vue3-apexcharts';
import net from "../../services/NetworkService";
import ENDPOINTS from "../../constants/endpoints";
import errors from '../../constants/errors';
import { EventBus } from "../../constants/eventBus";

export default {
    name: 'LatencyChart',
    components: {
        apexchart: ApexCharts,
    },
    props: {
        targetId: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            loading: true,
            target: null,
            statuslogs: [],
            series: [],
            chartOptions: {
                chart: {
                    type: 'line',
                    height: 350,
                    zoom: { enabled: true }
                },
                stroke: { curve: 'smooth' },
                xaxis: {
                    type: 'datetime',
                    labels: { format: 'dd/MM/yy HH:mm' },
                    title: { text: 'Timestamp' }
                },
                yaxis: {
                    title: { text: 'Response Time (ms)' }
                },
                tooltip: {
                    x: { format: 'dd/MM/yy HH:mm' }
                },
                legend: {
                    position: 'top'
                }
            }
        };
    },
    watch: {
        targetId: {
            immediate: true,
            handler() {
                this.fetchData();
            }
        }
    },
    mounted() {
        EventBus.on('refresh-targets', this.fetchData);
    },
    beforeUnmount() {
        EventBus.off('refresh-targets', this.fetchData);
    },
    methods: {
        async fetchData() {
            if (!this.targetId) return;
            this.loading = true;
            try {
                const [targetRes, logsRes] = await Promise.all([
                    net.get(`${ENDPOINTS.TARGET}${this.targetId}`),
                    net.get(`${ENDPOINTS.STATUS_LOGS}?target_id=${this.targetId}`)
                ]);

                this.target = targetRes.data;
                this.statuslogs = logsRes.data;

                this.generateSeries();
            } catch (e) {
                errors.value.push({
                    type: 'danger',
                    message: `Failed to load data for target ID ${this.targetId}.`
                });
            } finally {
                this.loading = false;
            }
        },

        generateSeries() {
            const data = this.statuslogs.map(log => ({
                x: new Date(log.timestamp).getTime(),
                y: log.response_time_ms
            }));

            this.series = [{
                name: this.target?.name || `Target ${this.targetId}`,
                data
            }];
        }
    }
};
</script>

<template>
    <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading target details...</p>
    </div>
    <div v-else>
        <apexchart type="line" height="350" :options="chartOptions" :series="series" />
    </div>
</template>
