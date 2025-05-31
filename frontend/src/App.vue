<script>
    import "./assets/vendors/bootstrap/css/bootstrap.min.css"
    import "./assets/vendors/bootstrap-icons/bootstrap-icons.css"
    import "./assets/vendors/boxicons/css/boxicons.min.css"
    import "./assets/vendors/quill/quill.snow.css"
    import "./assets/vendors/quill/quill.bubble.css"
    import "./assets/vendors/remixicon/remixicon.css"
    import "./assets/vendors/simple-datatables/style.css"

    import "./assets/css/style.css"


  import "./assets/vendors/apexcharts/apexcharts.min.js"
  import "./assets/vendors/bootstrap/js/bootstrap.bundle.min.js"
  import "./assets/vendors/chart.js/chart.umd.js"
  import "./assets/vendors/echarts/echarts.min.js"
  import "./assets/vendors/quill/quill.js"
  import "./assets/vendors/simple-datatables/simple-datatables.js"
  import "./assets/vendors/tinymce/tinymce.min.js"
  import "./assets/vendors/php-email-form/validate.js"

  import "./assets/js/main.js"

import ErrorLayout from './Layouts/ErrorLayout.vue'


  export default {
    name: 'Dashboard',
    components: {
      ErrorLayout
    }
  }
</script>

<template>
 <ErrorLayout
  code="500"
  message="Internal server error"
 />
</template>

<style scoped>
</style>
