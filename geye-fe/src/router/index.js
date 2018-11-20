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
    path: "/*",
    component: resolve => require(["../components/404.vue"], resolve),
  }
];

const router = new Router({
  mode: "history",
  routes: routerConf,
});

export default router;
