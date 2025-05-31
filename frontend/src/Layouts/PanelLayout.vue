<script>
import PanelHeader from '../components/ui/PanelHeader.vue';
import PanelSidebar from '../components/ui/PanelSidebar.vue';


export default {
  name: 'PanelLayout',
  components: {
    PanelHeader,
    PanelSidebar,
  },
  props: {
    title: {
      type: String,
      required: true
    },
    breadcrumb: {
      type: Array,
      required: true
    }
  },
  watch: {
    title(newTitle) {
      document.title = newTitle;
    }
  },
  created() {
    document.title = this.title;
  }
}
</script>

<template>
  <PanelHeader />
  <PanelSidebar />


  <main id="main" class="main">

    <div class="pagetitle">
      <h1>{{ title }}</h1>
      <nav>
        <ol class="breadcrumb">
          <li v-for="(item, index) in breadcrumb" :key="index" class="breadcrumb-item"
            :class="{ active: index === breadcrumb.length - 1 }">
            <a v-if="index !== breadcrumb.length - 1" href="#">{{ item }}</a>
            <span v-else>{{ item }}</span>
          </li>
        </ol>
      </nav>
    </div>

    <section class="section dashboard">
      <slot />
    </section>
  </main>

</template>
