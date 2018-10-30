<template>
  <div class="sidebar">
    <el-menu class="sidebar-el-menu" background-color="#324157"
             text-color="#bfcbd9" active-text-color="#20a0ff" :collapse="collapse">

      <template v-for="item in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="item.index">
            <template slot="title">
              <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-menu-item :index="subItem.index" :key="subItem.index">
                <span slot="title">{{ subItem.title }}</span>
              </el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index">
            <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </template>

    </el-menu>
  </div>
</template>

<script>
  import globalData from "./data";

  export default {
    name: "Sidebar",
    data() {
      return {
        collapse: false,
        items: [
          {
            icon: "el-icon-menu",
            index: "dashboard",
            title: "Dashboard",
          },
          {
            icon: "el-icon-menu",
            index: "rule-management",
            title: "规则管理",
            subs: [
              {
                index: "global-filter-rule-management",
                title: "全局过滤规则管理",
              },
              {
                index: "search-rule-management",
                title: "搜索规则管理",
              },
              {
                index: "monitor-management",
                title: "重点监控管理",
              }
            ]
          },
          {
            icon: "el-icon-menu",
            index: "handle-center",
            title: "处理中心"
          }
        ]
      }
    },
    created() {
      globalData.$on("collapse", msg => {
        console.log("receive message: " + msg);
        this.collapse = msg;
      })
    }
  }
</script>

<style scoped>
  .sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .sidebar::-webkit-scrollbar {
    width: 0;
  }

  .sidebar-el-menu:not(.el-menu--collapse) {
    width: 200px;
  }

  .sidebar > ul {
    height: 100%;
  }
</style>
