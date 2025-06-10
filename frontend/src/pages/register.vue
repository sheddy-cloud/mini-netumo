<script>
import RegistrationForm from '../components/forms/RegistrationForm.vue'; // Import the RegistrationForm component

export default {
    name: "RegisterPage",
    components: {
        RegistrationForm
    },
    data() {
        return {
            pageErrorMessage: '', // For displaying errors from the form component
        };
    },
    methods: {
        // Handler for a successful registration event from RegistrationForm
        handleRegistrationSuccess(newUser) {
            console.log('Registration successful for user:', newUser);
            this.pageErrorMessage = ''; // Clear any previous errors
            // After successful registration, redirect to login page
            this.$router.push({ name: 'Login' });
        },
        // Handler for errors emitted by RegistrationForm
        handleRegistrationError(errorMsg) {
            this.pageErrorMessage = errorMsg;
            // Optionally, clear the error message after a few seconds
            setTimeout(() => { this.pageErrorMessage = ''; }, 5000);
        },
    },
};
</script>

<template>
    <div class="registration-page-container">
        <div v-if="pageErrorMessage" class="alert alert-danger text-center">{{ pageErrorMessage }}</div>

        <RegistrationForm
            @registration-success="handleRegistrationSuccess"
            @error="handleRegistrationError"
        />
    </div>
</template>

<style scoped>
.registration-page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f0f2f5;
    padding: 20px;
    flex-direction: column;
}
.alert {
    margin-bottom: 20px;
    width: auto;
    max-width: 450px; /* Match form width */
    text-align: center;
}
.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}
</style>
