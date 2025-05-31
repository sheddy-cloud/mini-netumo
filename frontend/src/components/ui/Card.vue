<script>
export default {
  name: 'CardWrapper',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
};
</script>

<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title" v-if="title">{{ title }}</h5>
      <slot />
    </div>
  </div>
</template>
