<script>
export default {
  name: 'CardWrapper',
  props: {
    title: {
      type: String,
      default: ''
    }
  },
  // Add inheritAttrs: false to prevent Vue from automatically adding attrs to root,
  // then manually bind them below. This gives you more control.
  inheritAttrs: false
};
</script>

<template>
  <div class="card" v-bind="$attrs">
    <div class="card-body">
      <h5 class="card-title" v-if="title">{{ title }}</h5>
      <slot />
    </div>
  </div>
</template>