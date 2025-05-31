<script>
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import net from '../../services/NetworkService'; // Assuming NetworkService is your 'net'
import errors from '../../constants/errors'; // Assuming errors is your global error handler
import ENDPOINTS from '../../constants/endpoints'; // Assuming you have an ENDPOINTS constant for login

export default {
    name: "LoginForm",
    components: {
        BlankFormLayout,
    },
    data() {
        return {
            username: '', // Can be used for email or a username
            password: '',
            loading: false, // Add loading state
        };
    },
    methods: {
        async handleLogin() {
            this.loading = true; // Set loading to true on submission
            errors.value = []; // Clear previous errors using the global errors object

            if (!this.username.trim() || !this.password.trim()) {
                errors.value.push({ type: "danger", message: "Please enter both username/email and password." });
                this.loading = false;
                return;
            }

            try {
                // Call the login endpoint using net.post
                const user = await net.get(ENDPOINTS.LOGIN, { // Assuming ENDPOINTS.LOGIN is defined
                    username: this.username,
                    password: this.password,
                });

                errors.value.push({ type: "success", message: 'Login successful!' });
                // Clear inputs on success
                this.username = '';
                this.password = '';
            } catch (err) {
                errors.value.push({ type: "danger", message: `Login failed: ${backendMessage}.` });
            } finally {
                this.loading = false; // Set loading to false after submission
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
            <div v-if="loading" class="card-body">...</div>
            <div class="card-body">
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username or Email</label>
                        <input
                            type="text"
                            class="form-control"
                            id="username"
                            v-model="username"
                            placeholder="Enter your username or email"
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
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>

                <p class="mt-3 text-center">
                    Don't have an account? <router-link to="/register">Register here</router-link>
                </p>
            </div>
        </div>
    </BlankFormLayout>
</template>