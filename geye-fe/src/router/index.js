import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

const routerConf = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/hello",
    component: resolve => require(["../components/HelloWorld.vue"], resolve),
  },
  {
    path: "/rule/search/all",
    component: resolve => require(["../components/searchRule/all.vue"], resolve),
    name: "all-search-rule",
  },
  {
    path: "/rule/search/new",
    component: resolve => require(["../components/searchRule/new.vue"], resolve),
    name: "new-search-rule",
  },
  {
    path: "/rule/search/edit/:srid",
    component: resolve => require(["../components/searchRule/edit.vue"], resolve),
    name: "edit-search-rule",
  },

  {
    path: "/rule/global/filter",
    component: resolve => require(["../components/globalFilterRule.vue"], resolve),
    name: "global-filter-rule",
  },

  {
    path: "/rule/special-monitor",
    component: resolve => require(["../components/SpecialMonitor.vue"], resolve),
    name: "special-monitor",
  },

  {
    path: "/handleCenter/search",
    component: resolve => require(["@/components/handleCenter/SearchCenter.vue"], resolve),
    name: "handle-center-search",
  },

  {
    path: "/token",
    component: resolve => require(["@/components/token/token.vue"], resolve),
    name: "token",
  },

  {
    path: "/leaks",
    component: resolve => require(["@/components/leaks.vue"], resolve),
    name: "leaks",
  },

  {
    path: "/*",
    component: resolve => require(["../components/404.vue"], resolve),
  }
];

const router = new Router({
  mode: "history",
  routes: routerConf,
});

export default router;
