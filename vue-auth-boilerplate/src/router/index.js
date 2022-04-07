import Vue from "vue";
import Router from "vue-router";
import store from "../store";
import Login from "@/views/auth/login";
import Register from "@/views/auth/register";
import App from "@/views/layouts/App";
import Home from "@/views/home";
import DataScientist from "@/views/home/datascientist.vue";
import PlatformAdmin from "@/views/home/platformadmin.vue";
import EndUser from "@/views/home/enduser.vue";
import AppDeveloper from "@/views/home/appdeveloper.vue";
Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/login");
};

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "app",
      component: App,
      beforeEnter: ifAuthenticated,
      children: [
        {
          path: "/",
          name: "home",
          component: Home,
          children:[
            {
              path:"/datascientist",
              name:"datascientist",
              component:DataScientist,
            },
            {
              path:"/platformadmin",
              name:"platformadmin",
              component:PlatformAdmin,
            },
            {
              path:"/enduser",
              name:"enduser",
              component:EndUser,
            },
            {
              path:"/appdeveloper",
              name:"appdeveloper",
              component:AppDeveloper,
            }
          ]

        }
      ]
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/register",
      name: "register",
      component: Register,
      beforeEnter: ifNotAuthenticated
    }
  ]
});
