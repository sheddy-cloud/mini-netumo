<script>
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import net from '../../services/NetworkService'; // Network request handler
import errors from '../../constants/errors'; // Global error store
import ENDPOINTS from '../../constants/endpoints'; // API endpoints
import { login } from '../../services/AuthenticationService';

export default {
    name: "LoginForm",
    components: {
        BlankFormLayout,
    },
    data() {
        return {
            name: '',
            password: '',
            loading: false,
        };
    },
    methods: {
        async handleLogin() {
            this.loading = true;
            errors.value = []; // Clear previous errors

            if (!this.name.trim() || !this.password.trim()) {
                errors.value.push({ type: "danger", message: "Please enter both username/email and password." });
                this.loading = false;
                return;
            }

            try {
                // Use POST instead of GET
                await login(this.name, this.password)

                errors.value.push({ type: "success", message: 'Login successful!' });
                this.name = '';
                this.password = '';
            } catch (err) {
                const message = err?.response?.data?.detail || 'Unexpected error occurred.';
                errors.value.push({ type: "danger", message: `Login failed: ${message}` });
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<template>
    <BlankFormLayout>
        <div class="card login-form-component">
            <div class="card-header">
                <h4>Login to Mini-Netumo</h4>
            </div>
            <div v-if="loading" class="card-body">
                <p>Loading...</p>
            </div>
            <div class="card-body" v-else>
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label for="name" class="form-label">Username or Email</label>
                        <input
                            type="email"
                            class="form-control"
                            id="name"
                            v-model="name"
                            placeholder="Enter your name or email"
                            required

                        />
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input
                            type="password"
                            class="form-control"
                            id="password"
                            v-model="password"
                            placeholder="Enter your password"
                            required
                        />
                    </div>
                    <button type="button" class="btn btn-primary w-100" :disabled="loading" @click="handleLogin">
                        {{ loading ? "Logging in..." : "Login" }}
                    </button>
                </form>

                <p class="mt-3 text-center">
                    Don't have an account? <router-link to="/register">Register here</router-link>
                </p>
            </div>
        </div>
    </BlankFormLayout>
</template>
