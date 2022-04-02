import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueSnackbar from "vue-snack";
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import ButtonSpinner from "@/components/globals/ButtonSpinner";
import VueFormulate from '@braid/vue-formulate'

UIkit.use(Icons);
window.UIkit = UIkit;

// loads the Icon plugin
window._ = require("lodash");

require("./styles/index.scss");
require('../node_modules/@braid/vue-formulate/themes/snow/snow.scss');
require("vue-snack/dist/vue-snack.min.css");

Vue.config.productionTip = false;

window.Event = new Vue();

Vue.use(VueSnackbar, {});



Vue.use(VueFormulate)

Vue.component("button-spinner", ButtonSpinner);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
