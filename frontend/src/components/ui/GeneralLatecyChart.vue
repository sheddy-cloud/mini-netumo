<script>
import ApexCharts from 'vue3-apexcharts'
import net from "../../services/NetworkService"
import ENDPOINTS from "../../constants/endpoints"
import errors from '../../constants/errors';
import { EventBus } from "../../constants/eventBus";

export default {
  name: 'GeneralLatencyChart',
  components: {
    apexchart: ApexCharts,
  },
  data() {
    return {
      loading: true,
      targets: [],
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
  mounted() {
    this.fetchData();
    EventBus.on('refresh-targets', this.fetchData)
  },

  destroyed(){
    EventBus.off('refresh-targets', this.fetchData)
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const [targetsRes, logsRes] = await Promise.all([
          net.get(ENDPOINTS.TARGET),
          net.get(ENDPOINTS.STATUS_LOGS)
        ]);

        this.targets = targetsRes.data;
        this.statuslogs = logsRes.data;

        this.generateSeries();

      } catch (e) {
        errors.value.push({
          type: 'danger',
          message: 'Failed to load targets or logs for the latency chart.'
        });
      } finally {
        this.loading = false;
      }
    },

    generateSeries() {
      const nameMap = Object.fromEntries(
        this.targets.map(t => [t.id, t.name])
      );

      const seriesMap = {};

      for (const log of this.statuslogs) {
        const name = nameMap[log.target_id];
        if (!name) continue;

        if (!seriesMap[name]) {
          seriesMap[name] = [];
        }

        seriesMap[name].push({
          x: new Date(log.timestamp).getTime(),
          y: log.response_time_ms
        });
      }

      this.series = Object.entries(seriesMap).map(([name, data]) => ({
        name,
        data
      }));
    }
  }
};
</script>

<template>
  <div v-if="loading">Loading chart...</div>
  <div v-else>
    <apexchart type="line" height="350" :options="chartOptions" :series="series" />
  </div>
</template>
