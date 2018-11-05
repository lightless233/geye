<template>
  <div class="wrapper" id="app">
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
  @import "assets/css/main.css";
  @import "assets/css/color-dark.css";
</style>


<script>
  import Header from "@/components/common/Header";
  import Sidebar from "@/components/common/Sidebar";
  import GlobalData from "./components/common/data";

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
    },
    created() {
      GlobalData.$on("collapse", msg => {
        this.collapse = msg;
      })
    }
  }
</script>
