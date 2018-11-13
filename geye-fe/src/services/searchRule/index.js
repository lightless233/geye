import config from "@/config";

const BASE_API = config.BASE_API;
const API_LIST = {
  all: BASE_API + "/api/v1/rule/search/all",
  addSearchRule: BASE_API + "/api/v1/rule/search/new",
};


const services = {
  all(context) {
    return context.axios.get(API_LIST.all);
  },
  addSearchRule(context, data) {
    return context.axios.post(API_LIST.addSearchRule, data, {withCredentials: true});
  }
};

export default services
