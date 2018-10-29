<template>
  <div class="el-header">
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="collapseChange">
      <i class="el-icon-menu"></i>
    </div>
    <!-- ./折叠按钮 -->

    <div class="logo">GEYE Management System</div>
    <div class="header-right">
      <div class="header-user-con"></div>
    </div>

  </div>
</template>

<script>
  export default {
    name: "Header",
    data() {
      return {
        collapse: false,
        fullscreen: false,
        name: "xxx",
        message: 2
      }
    },
    computed: {
      username() {
        let username = localStorage.getItem("geye_username");
        return username ? username : this.name;
      }
    },
    methods: {
      collapseChange() {
        this.collapse = !this.collapse;
        //
      }
    },
    mounted() {
      if (document.body.clientWidth < 1500) {
        this.collapseChange();
      }
    }
  }
</script>

<style scoped>

</style>
