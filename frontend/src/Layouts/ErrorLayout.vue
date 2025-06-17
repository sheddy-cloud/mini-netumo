<script>
import errorImage from "../assets/img/not-found.png";

export default {
  name: "ErrorLayout",
  props: {
    code: {
      type: String,
      required: false,
    },
    message: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      errorImage
    }
  }
}
</script>

<template>
  <main>
    <div class="container">

      <section class="section error-404 min-vh-100 d-flex flex-column align-items-center justify-content-center">
        <h1>{{ code }}</h1>
        <h2>{{ message }}.</h2>
        <router-link to="/home">
          <div class="btn btn-info">Back to home</div>
        </router-link>
        <img :src="errorImage" class="img-fluid py-5" alt="Page Not Found">
        <div class="credits">
          Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
        </div>
      </section>

    </div>
  </main>
</template>
