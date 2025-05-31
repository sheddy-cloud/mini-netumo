<script>
// Adjust path to BlankFormLayout based on its actual location relative to components/forms
import BlankFormLayout from '../../Layouts/BlankFormLayout.vue';
import { registerUser } from '../../services/monitorService'; // Assuming registerUser is in monitorService.js

export default {
    name: "RegistrationForm",
    components: {
        BlankFormLayout
    },
    // Define the events this component can emit
    emits: ['registration-success', 'error'],
    data() {
        return {
            name: '',
            email: '',
            password: '',
            formErrorMessage: '',
            formSuccessMessage: '',
        };
    },
    methods: {
        async handleRegistration() {
            this.formErrorMessage = ''; // Clear previous errors
            this.formSuccessMessage = '';

            // Basic validation
            if (!this.name.trim() || !this.email.trim() || !this.password.trim()) {
                this.formErrorMessage = 'All fields are required.';
                return;
            }

            // Simple email validation (can be more robust)
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.email)) {
                this.formErrorMessage = 'Please enter a valid email address.';
                return;
            }

            // Password strength validation (example: min 6 characters)
            if (this.password.length < 6) {
                this.formErrorMessage = 'Password must be at least 6 characters long.';
                return;
            }

            try {
                // Call the registerUser function from your service
                const newUser = await registerUser({
                    name: this.name,
                    email: this.email,
                    password: this.password,
                });

                this.formSuccessMessage = 'Registration successful! You can now log in.';
                // Clear inputs on success
                this.name = '';
                this.email = '';
                this.password = '';
                // Emit a success event to the parent
                this.$emit('registration-success', newUser);
            } catch (err) {
                console.error("Error during registration:", err);
                const backendMessage = err.response?.data?.message || err.message;
                this.formErrorMessage = `Registration failed: ${backendMessage}.`;
                // Emit an error event to the parent
                this.$emit('error', this.formErrorMessage);
            }
        },
    },
};
</script>

<template>
    <BlankFormLayout>
        <div class="registration-container">
            <h2>Register for Mini-Netumo</h2>

            <div v-if="formSuccessMessage" class="alert alert-success">{{ formSuccessMessage }}</div>
            <div v-if="formErrorMessage" class="alert alert-danger">{{ formErrorMessage }}</div>

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
    </BlankFormLayout>
</template>

<style scoped>
.registration-container {
    max-width: 450px; /* Slightly wider for more fields */
    margin: auto; /* Center content within BlankFormLayout */
    padding: 2.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    background-color: #fff;
}

h2 {
    text-align: center;
    margin-bottom: 2rem;
    color: #333;
    font-size: 1.8rem;
}

.alert {
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
    font-size: 0.9rem;
}
.alert-success {
    color: #0f5132;
    background-color: #d1e7dd;
    border-color: #badbcc;
}
.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}

.form-label {
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: block;
}

.form-control {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.form-control:focus {
    color: #495057;
    background-color: #fff;
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
    color: white;
    padding: 0.75rem 1.25rem;
    font-size: 1.1rem;
    border-radius: 0.3rem;
    transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}
.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

.mt-3 {
    margin-top: 1rem !important;
}
.text-center {
    text-align: center !important;
}
</style>
