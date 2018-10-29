<template>
  <div class="wrapper">
    <v-head></v-head>
    <v-sidebar></v-sidebar>
    <div class="content-box" :class="{'content-collapse': collapse}">
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<style>

</style>


<script>
  import Header from "@/components/common/Header";
  import Sidebar from "@/components/common/Sidebar";

  export default {
    name: "Home",
    components: {
      "v-head": Header,
      "v-sidebar": Sidebar,
    },
    data() {
      return {
        collapse: false,
      }
    }
  }
</script>
