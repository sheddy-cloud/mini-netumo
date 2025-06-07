<script>
import { EventBus } from '../../constants/eventBus';
import EditTargetForm from '../forms/EditTargetForm.vue';
import errors from '../../constants/errors';
import net from '../../services/NetworkService';
import ENDPOINTS from '../../constants/endpoints';

export default {
    name: "TargetsTable",
    components: {
        EditTargetForm,
    },
    data() {
        return {
            targets: [],
            selectedTarget: null,
            showEditModal: false,
            showDeleteModal: false,
            searchQuery: '',
            pageSize: 10,
            currentPage: 1,
        };
    },
    mounted() {
        this.fetchTargets();
        EventBus.on('refresh-targets', this.fetchTargets)
    },
    destroyed() {
        EventBus.off('refresh-targets', this.fetchTargets)
    },
    methods: {
        async fetchTargets() {
            try {
                const res = await net.get(ENDPOINTS.TARGET);
                this.targets = res.data;
            } catch (e) {
                errors.value.push({
                    type: "danger",
                    message: "Failed to load targets."
                });
            }
        },
        openEditModal(target) {
            this.selectedTarget = target;
            this.showEditModal = true;
        },
        openDeleteModal(target) {
            this.selectedTarget = target;
            this.showDeleteModal = true;
        },
        closeModals() {
            this.showEditModal = false;
            this.showDeleteModal = false;
            this.selectedTarget = null;
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
        changePageSize(size) {
            this.pageSize = size;
            this.currentPage = 1;
        },
        async deleteTarget() {
            if (!this.selectedTarget) return;

            try {
                await net.delete(`${ENDPOINTS.TARGET}${this.selectedTarget.target_id}`);
                this.closeModals();
                errors.value.push({
                    type: "success",
                    message: `Deleted  Successfully`
                })
                EventBus.emit('refresh-targets');
            } catch (e) {
                errors.value.push({
                    type: "danger",
                    message: `Failed to delete .`,
                });
            }
        },

    },
    computed: {
        filteredTargets() {
            if (!this.searchQuery) return this.targets;
            const query = this.searchQuery.toLowerCase();
            return this.targets.filter(target =>
                target.name.toLowerCase().includes(query) ||
                target.url.toLowerCase().includes(query)
            );
        },
        paginatedTargets() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredTargets.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.filteredTargets.length / this.pageSize);
        }
    }
};
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
                <input type="text" class="form-control" placeholder="Search targets..." v-model="searchQuery" />
            </div>
            <div>
                <label class="me-2">Page Size:</label>
                <select class="form-select d-inline-block w-auto" v-model.number="pageSize">
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                </select>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-striped align-middle">
                <thead class="table-light">
                    <tr>
                        <th>Name</th>
                        <th>URL</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="target in paginatedTargets" :key="target.target_id">
                        <td>
                            <router-link :to="`/targets/${target.target_id}`">
                                {{ target.name }}
                            </router-link>
                        </td>
                        <td>
                            <a :href="target.url" target="_blank" rel="noopener noreferrer">
                                {{ target.url }}
                                <i class="bi bi-box-arrow-up-right ms-1" aria-label="Opens in new tab"></i>
                            </a>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="openEditModal(target)">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" @click="openDeleteModal(target)">
                                <i class="bi bi-trash"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <nav class="mt-3" style="margin-right: auto;">
            <ul class="pagination justify-content-start">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="goToPage(currentPage - 1)">Previous</button>
                </li>

                <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
                    <button class="page-link" @click="goToPage(page)">{{ page }}</button>
                </li>

                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link" @click="goToPage(currentPage + 1)">Next</button>
                </li>
            </ul>
        </nav>

        <!-- Edit Modal -->
        <div class="modal fade show" v-if="showEditModal" style="display: block;" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Edit Target</h5>
                        <button type="button" class="btn-close" @click="closeModals"></button>
                    </div>
                    <div class="modal-body">
                        <EditTargetForm :target="selectedTarget" @target-updated="closeModals" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div class="modal fade show" v-if="showDeleteModal" style="display: block;" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Target</h5>
                        <button type="button" class="btn-close" @click="closeModals"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete <strong>{{ selectedTarget?.name }}</strong>?</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="closeModals">Cancel</button>
                        <button class="btn btn-danger" @click="deleteTarget">
                            <i class="bi bi-trash me-1"></i> Confirm Delete
                        </button>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal {
    background: rgba(0, 0, 0, 0.5);
}
</style>
