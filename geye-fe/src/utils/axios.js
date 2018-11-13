import axios from "axios"
import CSRF_API from "../services"
import config from "@/config"

axios.defaults.timeout = 5000;
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
const BASE_API = config.BASE_API;


function getCSRFToken(config) {
  return axios.get(BASE_API + CSRF_API)
    .then(response => {
      // console.log("CSRF Token API response:", response.data);
      config.withCredentials = true;
      config.headers["X-CSRFToken"] = response.data.trim();
      return config;
    })
}

// request 拦截器
axios.interceptors.request.use(
  config => {
    // todo: 这里先简单判断，后面需要优化掉
    // console.log(config);
    if (config.url.indexOf(CSRF_API) > -1 || config.method !== "post") {
      // console.log("no need csrf!");
      return config;
    }

    // POST和PUT请求需要先请求CSRF Token
    if (config.method === "post" || config.method === "put") {
      return getCSRFToken(config);
    }
  }
);

export default axios