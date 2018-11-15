import config from "@/config";

const BASE_API = config.BASE_API;
const API_LIST = {
  all: BASE_API + "/api/v1/rule/search/all",
  addSearchRule: BASE_API + "/api/v1/rule/search/new",
  deleteSearchRule: BASE_API + "/api/v1/rule/search/delete",
  changeSearchRuleStatus: BASE_API + "/api/v1/rule/search/change_status",
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
  },

  // 修改某个search rule 的状态
  changeStatus(context, id) {
    return context.axios.post(API_LIST.changeSearchRuleStatus, id)
  },

};

export default services
