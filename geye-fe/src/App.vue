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
  @import "../static/css/main.css";
  @import "../static/css/color-dark.css";
  @import "../node_modules/@fortawesome/fontawesome-free/css/fontawesome.min.css";
  @import
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
