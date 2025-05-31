<style></style>

<script>
import BlankFormLayout from "../../Layouts/BlankFormLayout.vue"

export default {
    name: "LoginForm",
    components: {
        BlankFormLayout
    }
}
</script>

<template>
    <BlankFormLayout>
        <h2>Mini-Netumo</h2>
        <router-link to="/home">
            <div class="btn btn-primary">Login</div>
        </router-link>
    </BlankFormLayout>
</template>
