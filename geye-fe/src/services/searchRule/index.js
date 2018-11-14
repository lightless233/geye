import config from "@/config";

const BASE_API = config.BASE_API;
const API_LIST = {
  all: BASE_API + "/api/v1/rule/search/all",
  addSearchRule: BASE_API + "/api/v1/rule/search/new",
  deleteSearchRule: BASE_API + "/api/v1/rule/search/delete",
};


const services = {

  all(context) {
    return context.axios.get(API_LIST.all);
  },

  addSearchRule(context, data) {
    return context.axios.post(API_LIST.addSearchRule, data, {withCredentials: true});
  },

  deleteSearchRule(context, id) {
    return context.axios.post(API_LIST.deleteSearchRule, id)
  }

};

export default services
