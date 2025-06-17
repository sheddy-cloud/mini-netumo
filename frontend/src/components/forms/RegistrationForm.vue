<script>
// Adjust path to BlankFormLayout based on its actual location relative to components/forms
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import net from '../../services/NetworkService'; // Assuming NetworkService is your 'net'
import errors from '../../constants/errors'; // Assuming errors is your global error handler
import ENDPOINTS from '../../constants/endpoints'; // Assuming you have an ENDPOINTS constant for registration

export default {
    name: "RegistrationForm",
    components: {
        BlankFormLayout,
    },
    emits: ['registration-success', 'error'],
    data() {
        return {
            name: '',
            email: '',
            password: '',
            loading: false, // Add loading state
        };
    },
    methods: {
        async handleRegistration() {
            this.loading = true; // Set loading to true on submission
            errors.value = []; // Clear previous errors using the global errors object

            // Basic validation
            if (!this.name.trim()) {
                errors.value.push({ type: "danger", message: "Full Name cannot be empty." });
                this.loading = false;
                return;
            }
            if (!this.email.trim()) {
                errors.value.push({ type: "danger", message: "Email Address cannot be empty." });
                this.loading = false;
                return;
            }
            if (!this.password.trim()) {
                errors.value.push({ type: "danger", message: "Password cannot be empty." });
                this.loading = false;
                return;
            }

            // Simple email validation (can be more robust)
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.email)) {
                errors.value.push({ type: "danger", message: "Please enter a valid email address." });
                this.loading = false;
                return;
            }

            // Password strength validation (example: min 6 characters)
            if (this.password.length < 6) {
                errors.value.push({ type: "danger", message: "Password must be at least 6 characters long." });
                this.loading = false;
                return;
            }

            try {
                // Call the registerUser function from your service, using net.post
                const newUser = await net.post(ENDPOINTS.REGISTER, { // Assuming ENDPOINTS.REGISTER is defined
                    name: this.name,
                    email: this.email,
                    password: this.password,
                });

                errors.value.push({ type: "success", message: 'Registration successful! You can now log in.' });
                // Clear inputs on success
                this.name = '';
                this.email = '';
                this.password = '';
                // Emit a success event to the parent
                this.$emit('registration-success', newUser);
            } catch (err) {
                errors.value.push({ type: "danger", message: `Registration failed.` });
            } finally {
                this.loading = false; // Set loading to false after submission
            }
        },
    },
};
</script>

<template>
    <BlankFormLayout>
        <div class="card registration-form-component">
            <div class="card-header">
                <h4>Register for Mini-Netumo</h4>
            </div>
            <div v-if="loading" class="card-body">...</div>
            <div class="card-body">
                <form @submit.prevent="handleRegistration">
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input
                            type="text"
                            class="form-control"
                            id="name"
                            v-model="name"
                            placeholder="Enter your full name"
                            required
                        />
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email Address</label>
                        <input
                            type="email"
                            class="form-control"
                            id="email"
                            v-model="email"
                            placeholder="Enter your email"
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
                            placeholder="Create a password"
                            required
                        />
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>

                <p class="mt-3 text-center">
                    Already have an account? <router-link to="/login">Login here</router-link>
                </p>
            </div>
        </div>
    </BlankFormLayout>
</template>
