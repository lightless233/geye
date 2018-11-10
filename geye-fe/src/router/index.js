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
  },
  {
    path: "/rule/search/new",
    component: resolve => require(["../components/searchRule/new.vue"], resolve),
    name: "new-search-rule",
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

// import Vue from "vue";
// import Router from "vue-router";
// import Home from "./views/Home.vue";
//
// Vue.use(Router);
//
// export default new Router({
//   mode: "history",
//   base: process.env.BASE_URL,
//   routes: [
//     {
//       path: "/",
//       name: "home",
//       component: Home
//     },
//     {
//       path: "/about",
//       name: "about",
//       // route level code-splitting
//       // this generates a separate chunk (about.[hash].js) for this route
//       // which is lazy-loaded when the route is visited.
//       component: () =>
//         import(/* webpackChunkName: "about" */ "./views/About.vue")
//     }
//   ]
// });
