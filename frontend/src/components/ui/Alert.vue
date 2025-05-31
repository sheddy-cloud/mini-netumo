<template>
    <div :class="['alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show']" role="alert">
        <i :class="iconClass + ' me-1'"></i>
        {{ message }}
        <button type="button" class="btn-close" aria-label="Close" @click="closeAlert"></button>
    </div>
</template>

<script>

export default {
    name: "Alert",
    props: {
        type: {
            type: String,
            required: true,
            validator(value) {
                // restrict to valid Bootstrap alert types
                return [
                    "primary",
                    "secondary",
                    "success",
                    "danger",
                    "warning",
                    "info",
                    "dark",
                ].includes(value);
            },
        },
        message: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            isVisible: true,
        };
    },
    computed: {
        iconClass() {
            const icons = {
                primary: "bi bi-star",
                secondary: "bi bi-collection",
                success: "bi bi-check-circle",
                danger: "bi bi-exclamation-octagon",
                warning: "bi bi-exclamation-triangle",
                info: "bi bi-info-circle",
                dark: "bi bi-folder",
            };
            return icons[this.type] || "bi bi-info-circle";
        },
    },
    methods: {
        closeAlert() {
            this.$emit('close');
        }
    }

};
</script>

<style scoped>
.alert[style*="display: none"] {
    display: none !important;
}
</style>
