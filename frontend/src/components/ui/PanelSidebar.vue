<script>
import net from "../../services/NetworkService"
import ENDPOINTS from "../../constants/endpoints"
import errors from '../../constants/errors';
import { EventBus } from "../../constants/eventBus";

//data
export default {
    name: "PanelSidebar",

    data() {
        return {
            loading: true,
            targets: [],
        }
    },


    methods: {
        async fetchTargets() {
            try {
                const res = await net.get(ENDPOINTS.TARGET);
                this.targets = res.data
            } catch (e) {
                errors.value.push({ type: "danger", message: "There was an error while loading websites on the sidebar" })
            } finally {
                this.loading = false
            }
        }
    },

    created() {
        this.fetchTargets()
        EventBus.on('refresh-sidebar', this.fetchTargets);
    },

    beforeDestroy() {
        EventBus.off('refresh-sidebar', this.fetchTargets);
    },
}

</script>

<template>
    <aside id="sidebar" class="sidebar">

        <ul class="sidebar-nav" id="sidebar-nav">

            <li class="nav-item">
                <router-link to="/">
                    <div class="nav-link collapsed" href="index.html">
                        <i class="bi bi-grid"></i>
                        <span>Dashboard</span>
                    </div>
                </router-link>
            </li>

            <li class="nav-item">
                <a class="nav-link collapsed" data-bs-target="#components-nav" data-bs-toggle="collapse" href="#">
                    <i class="bi bi-menu-button-wide"></i><span>Websites</span><i
                        class="bi bi-chevron-down ms-auto"></i>
                </a>
                <ul id="components-nav" class="nav-content collapse " data-bs-parent="#sidebar-nav">
                    <li v-for="target in targets" :key="target.id">
                        <router-link :to="`/targets/${target.id}`">
                            <i class="bi bi-circle"></i><span>{{ target.name }}</span>
                        </router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </aside>
</template>
