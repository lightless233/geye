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
    path: "/rule/search-rule-management",
    component: resolve => require(["../components/rule/search-rule-management.vue"], resolve),
  },
  {
    path: "/*",
    component: resolve => require(["../components/404.vue"], resolve),
  }
];

const router = new Router({
  routes: routerConf,
});

export default router;
