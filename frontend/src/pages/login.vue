<script>
import LoginForm from '../components/forms/LoginForm.vue'; // Import the LoginForm component

export default {
    name: "LoginPage", // Changed name for clarity and consistency
    components: {
        LoginForm
    },
    data() {
        return {
            pageErrorMessage: '', // For displaying errors that come from the LoginForm component
        };
    },
    methods: {
        // Handler for a successful login event from LoginForm
        handleLoginSuccess(user) {
            console.log('Login successful for user:', user);
            this.pageErrorMessage = ''; // Clear any previous errors
            // Redirect to the dashboard page
            this.$router.push({ name: 'Dashboard' }); // Use the name 'Dashboard' as defined in your router/index.js
        },
        // Handler for errors emitted by LoginForm
        handleLoginError(errorMsg) {
            this.pageErrorMessage = errorMsg;
            // Optionally, clear the error message after a few seconds
            setTimeout(() => { this.pageErrorMessage = ''; }, 5000);
        },
    },
};
</script>

<template>
    <div class="login-page-container">
        <div v-if="pageErrorMessage" class="alert alert-danger text-center">{{ pageErrorMessage }}</div>

        <LoginForm
            @login-success="handleLoginSuccess"
            @error="handleLoginError"
        />
    </div>
</template>

<style scoped>
.login-page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh; /* Make sure it takes full viewport height */
    background-color: #f0f2f5; /* Light background for the login page */
    padding: 20px;
    flex-direction: column; /* Stack alert above form */
}
.alert {
    margin-bottom: 20px; /* Space between alert and form */
    width: auto;
    max-width: 400px; /* Match form width */
    text-align: center;
}
.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}
</style>
