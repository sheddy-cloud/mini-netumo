<script>
import logo from "../../assets/img/logo.png"
import net from '../../services/NetworkService';  // Your API service
import ENDPOINTS from '../../constants/endpoints';

export default {
    data() {
        return {
            logo,
            userName: 'Settings',  // default text before fetching real user name
        }
    },
    async mounted() {
        await this.fetchUserName();
    },
    methods: {
        toggle() {
            document.body.classList.toggle("toggle-sidebar");
        },
        logout() {
            localStorage.clear();
            sessionStorage.clear();
            this.$router.push('/login');
        },
        async fetchUserName() {
            try {
                const response = await net.get(ENDPOINTS.USER_PROFILE);
                this.userName = response.data.name || 'User';
            } catch (error) {
                console.error('Failed to fetch user name:', error);
                this.userName = 'User';
            }
        }
    }
}
</script>

<template>
    <header id="header" class="header fixed-top d-flex align-items-center">
        <div class="d-flex align-items-center justify-content-between">
            <router-link to="/">
                <div class="logo d-flex align-items-center">
                    <img :src="logo" alt="">
                    <span class="d-none d-lg-block">Mini-Netumo</span>
                </div>
            </router-link>
            <i class="bi bi-list toggle-sidebar-btn" @click="toggle"></i>
        </div>

        <nav class="header-nav ms-auto">
            <ul class="d-flex align-items-center">
                <li class="nav-item dropdown pe-3">
                    <a class="nav-link nav-profile d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown">
                        <!-- <img src="" alt="Profile" class="rounded-circle"> -->
                        <span class="d-none d-md-block dropdown-toggle ps-2">{{ userName }}</span>
                    </a>

                    <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile">
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item d-flex align-items-center" href="#" @click.prevent="logout">
                                <i class="bi bi-box-arrow-right"></i>
                                <span>Sign Out</span>
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>
        </nav>
    </header>
</template>
