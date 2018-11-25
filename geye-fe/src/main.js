import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import NormailizeCss from 'normalize.css'

// font awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTachometerAlt, faList, faPaperPlane, faBars, faKey } from '@fortawesome/free-solid-svg-icons'
import {faCircle} from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faTachometerAlt, faList, faPaperPlane, faCircle, faBars, faKey);


// axios
// import axios from "axios"
import axios from "./utils/axios"
import VueAxios from "vue-axios"

import App from './App'
import router from './router'


Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;
Vue.use(ElementUI);
// Vue.prototype.$axios = axios;
Vue.use(VueAxios, axios);

 /* eslint-disable */
new Vue({
  router,
  render: h => h(App),
}).$mount("#app");
