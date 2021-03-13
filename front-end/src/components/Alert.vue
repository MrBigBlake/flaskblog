<template>
  <div class="alert" role="alert" v-bind:class="'alert-' + variant"></div>
</template>

<script>
  export default {
    name: "Alert",
    props: ["variant", "message"]
  }
</script>

<style scoped>

</style>
