<script>
import logo from "../../assets/img/logo.png"
import net from "../../services/NetworkService"
import endpoints from "../../constants/endpoints"

//data
export default {
    name: "PanelSidebar",

    data(){
        return {
            loading: true,
            error: "",
            targets: [],
        }
    },

    methods: {
        async fetchTargets() {
            try{
                const res = await net.get(endpoints.TARGET);
                this.targets = res.data
            }catch (e){
                this.error = "There was an error while load targets"
            }finally {
                this.loading = false
            }
        }
    },

    created(){
        this.fetchTargets()
    }
}

</script>

<template>
        <aside id="sidebar" class="sidebar">

        <ul class="sidebar-nav" id="sidebar-nav">

            <li class="nav-item">
                <a class="nav-link collapsed" href="index.html">
                    <i class="bi bi-grid"></i>
                    <span>Dashboard</span>
                </a>
            </li><!-- End Dashboard Nav -->

            <li class="nav-item">
                <a class="nav-link collapsed" data-bs-target="#components-nav" data-bs-toggle="collapse" href="#">
                    <i class="bi bi-menu-button-wide"></i><span>Websites</span><i
                        class="bi bi-chevron-down ms-auto"></i>
                </a>
                <ul id="components-nav" class="nav-content collapse " data-bs-parent="#sidebar-nav">
                    <li v-for="target in targets" :key="target.target_id">
                        <router-link :to="`/targets/${target.target_id}`">
                            <i class="bi bi-circle"></i><span>{{ target.name }}</span>
                        </router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </aside>
</template>
