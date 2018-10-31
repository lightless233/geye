import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import NormailizeCss from 'normalize.css'

// font awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTachometerAlt, faList, faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import {faCircle} from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faTachometerAlt, faList, faPaperPlane, faCircle);


import App from './App'
import router from './router'


Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;
Vue.use(ElementUI);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
