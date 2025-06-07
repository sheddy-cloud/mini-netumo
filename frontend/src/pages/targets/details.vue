<script>
import PanelLayout from '../../Layouts/PanelLayout.vue';
import net from '../../services/NetworkService';
import ENDPOINTS from '../../constants/endpoints';
import Card from "../../components/ui/Card.vue"
import moment from 'moment'; // Import moment.js for date formatting and calculations
import LatencyChart from '../../components/ui/LatencyChart.vue';

export default {
    name: "target_details",
    props: ['id'],
    data() {
        return {
            loading: true,
            error: "",
            target: {},
            uptimePercentage: 'N/A',
            sslDaysLeft: 'N/A',
            registrationDaysLeft: 'N/A',
            recentStatusLogs: [],
            targetAlerts: [],
        }
    },
    methods: {
        async fetchTarget() {
            try {
                this.loading = true; // Reset loading state
                const res = await net.get(`${ENDPOINTS.TARGET}${this.id}`);
                this.target = res.data;
                // Once target is fetched, fetch related data
                await Promise.all([
                    this.fetchUptime(),
                    this.fetchSslAndRegistration(),
                    this.fetchRecentStatusLogs(),
                    this.fetchTargetAlerts()
                ]);
            } catch (e) {
                console.error("Error fetching target details:", e);
                this.error = "Failed to get detail for this website";
            } finally {
                this.loading = false;
            }
        },

        async fetchUptime() {
            try {
                // Assuming statuslogs are accessible via a target ID or you can filter them
                // For a more robust API, you'd have an endpoint like /targets/{id}/statuslogs
                const res = await net.get(ENDPOINTS.STATUS_LOGS + this.id);
                const targetLogs = res.data;

                if (targetLogs.length > 0) {
                    const successfulChecks = targetLogs.filter(log => log.status_code >= 200 && log.status_code < 300).length;
                    this.uptimePercentage = ((successfulChecks / targetLogs.length) * 100).toFixed(2) + '%';
                } else {
                    this.uptimePercentage = 'N/A';
                }
            } catch (e) {
                console.error("Error fetching uptime:", e);
                this.uptimePercentage = 'Error';
            }
        },

        async fetchSslAndRegistration() {
            try {
                const [domainRes, certRes] = await Promise.all([
                    net.get(ENDPOINTS.DOMAIN_CHECKS + this.id),
                    net.get(ENDPOINTS.CERTIFICATE_CHECKS + this.id)
                ]);

                const targetDomainCheck = domainRes.data;
                const targetCertCheck = certRes.data;

                if (targetDomainCheck) {
                    this.registrationDaysLeft = `${targetDomainCheck.days_remaining} days left`;
                } else {
                    this.registrationDaysLeft = 'N/A';
                }

                if (targetCertCheck) {
                    this.sslDaysLeft = `${targetCertCheck.days_remaining} days left`;
                } else {
                    this.sslDaysLeft = 'N/A';
                }

            } catch (e) {
                console.error("Error fetching SSL/Registration:", e);
                this.sslDaysLeft = 'Error';
                this.registrationDaysLeft = 'Error';
            }
        },

        async fetchRecentStatusLogs() {
            try {
                const res = await net.get(ENDPOINTS.STATUS_LOGS);
                const targetLogs = res.data
                    .filter(log => log.target_id == this.id)
                    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)) // Sort by most recent
                    .slice(0, 5); // Get the 5 most recent logs
                this.recentStatusLogs = targetLogs;
            } catch (e) {
                console.error("Error fetching recent status logs:", e);
                this.recentStatusLogs = [];
            }
        },

        async fetchTargetAlerts() {
            try {
                const res = await net.get(ENDPOINTS.ALERTS);
                const targetAlerts = res.data
                    .filter(alert => alert.target_id == this.id)
                    .sort((a, b) => new Date(b.sent_at) - new Date(a.sent_at)); // Sort by most recent
                this.targetAlerts = targetAlerts;
            } catch (e) {
                console.error("Error fetching target alerts:", e);
                this.targetAlerts = [];
            }
        },
        formatDate(dateString) {
            return moment(dateString).format('MMM Do, h:mm A');
        },
        getIconForStatusCode(statusCode) {
            if (statusCode >= 200 && statusCode < 300) {
                return 'bi-check-circle-fill text-success';
            } else if (statusCode >= 400 && statusCode < 500) {
                return 'bi-exclamation-triangle-fill text-warning';
            } else if (statusCode >= 500) {
                return 'bi-x-circle-fill text-danger';
            }
            return 'bi-question-circle-fill text-muted';
        },
        getAlertIcon(type) {
            switch (type) {
                case 'Downtime': return 'bi-cloud-slash-fill text-danger';
                case 'SSL Expiring': return 'bi-shield-fill-exclamation text-warning';
                default: return 'bi-bell-fill text-info';
            }
        }
    },
    created() {
        this.fetchTarget();
    },
    components: {
        PanelLayout,
        Card,
        LatencyChart
    },
    watch: {
        id(newId, oldId) {
            if (newId !== oldId) {
                this.fetchTarget();
            }
        }
    },
}
</script>


<template>
    <PanelLayout :title="target.name || '...'" :breadcrumb="['Websites', target.name || '...']">
        <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Loading target details...</p>
        </div>

        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>

        <div v-if="!loading && !error">
            <div class="row g-3 mb-4">
                <div class="col-md-4">
                    <Card title="Uptime" class="h-100">
                        <div class="d-flex align-items-center">
                            <div
                                class="card-icon rounded-circle d-flex align-items-center justify-content-center bg-primary-subtle text-primary">
                                <i class="bi bi-graph-up"></i>
                            </div>
                            <div class="ps-3">
                                <h6 class="mb-0">{{ uptimePercentage }}</h6>
                                <span class="text-muted small pt-2 ps-1">from all checks</span>
                            </div>
                        </div>
                    </Card>
                </div>

                <div class="col-md-4">
                    <Card title="SSL Expiry" class="h-100">
                        <div class="d-flex align-items-center">
                            <div
                                class="card-icon rounded-circle d-flex align-items-center justify-content-center bg-warning-subtle text-warning">
                                <i class="bi bi-shield-lock"></i>
                            </div>
                            <div class="ps-3">
                                <h6 class="mb-0">{{ sslDaysLeft }}</h6>
                                <span class="text-muted small pt-2 ps-1">until certificate expires</span>
                            </div>
                        </div>
                    </Card>
                </div>

                <div class="col-md-4">
                    <Card title="Domain Expiry" class="h-100">
                        <div class="d-flex align-items-center">
                            <div
                                class="card-icon rounded-circle d-flex align-items-center justify-content-center bg-success-subtle text-success">
                                <i class="bi bi-calendar-check"></i>
                            </div>
                            <div class="ps-3">
                                <h6 class="mb-0">{{ registrationDaysLeft }}</h6>
                                <span class="text-muted small pt-2 ps-1">until domain registration expires</span>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>

            <div class="row g-3">
                <div class="col-md-8">
                    <Card title="Latecy Chart">
                        <LatencyChart :targetId="id" />
                    </Card>
                </div>

                <div class="col-md-4">
                    <Card title="Recent Alerts" style="height: 450px; overflow-y: auto;">
                        <ul class="list-group list-group-flush">
                            <li v-if="targetAlerts.length === 0" class="list-group-item text-muted">
                                No recent alerts for this target.
                            </li>
                            <li v-for="alert in targetAlerts" :key="alert.id"
                                class="list-group-item d-flex justify-content-between align-items-start">
                                <div>
                                    <i :class="['bi', getAlertIcon(alert.type), 'me-2']"></i>
                                    <strong>{{ alert.type }}</strong>: {{ alert.message }}
                                </div>
                                <small class="text-muted text-end">{{ formatDate(alert.sent_at) }}</small>
                            </li>
                        </ul>
                    </Card>
                </div>
                <div>
                    <Card title="Recent Status Logs">
                        <ul class="list-group list-group-flush">
                            <li v-if="recentStatusLogs.length === 0" class="list-group-item text-muted">
                                No recent status logs available for this target.
                            </li>
                            <li v-for="log in recentStatusLogs" :key="log.id"
                                class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <i :class="['bi', getIconForStatusCode(log.status_code), 'me-2']"></i>
                                    Status: <strong>{{ log.status_code }}</strong> - Response Time: {{
                                        log.response_time_ms }}ms
                                </div>
                                <small class="text-muted">{{ formatDate(log.timestamp) }}</small>
                            </li>
                        </ul>
                    </Card>
                </div>
            </div>
        </div>
    </PanelLayout>
</template>

<style scoped>
/* Add some basic styling for the new card design */
.card-icon {
    width: 45px;
    height: 45px;
    font-size: 20px;
    margin-right: 15px;
}

/* Color variations for the card icons */
.bg-primary-subtle {
    background-color: #cfe2ff !important;
    /* Light blue */
}

.text-primary {
    color: #0d6efd !important;
}

.bg-warning-subtle {
    background-color: #fff3cd !important;
    /* Light yellow */
}

.text-warning {
    color: #ffc107 !important;
}

.bg-success-subtle {
    background-color: #d1e7dd !important;
    /* Light green */
}

.text-success {
    color: #198754 !important;
}
</style>
