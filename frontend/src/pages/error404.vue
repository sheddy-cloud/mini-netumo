<script>
import ErrorLayout from "../Layouts/ErrorLayout.vue"

export default {
    name: "error404",
    components: {
        ErrorLayout,
    }
}
</script>

<template>
    <ErrorLayout code="404" message="Oops. It's seems like you made a wrong turn"/>
</template>
