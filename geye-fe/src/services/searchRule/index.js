import config from "@/config";

const BASE_API = config.BASE_API;
const API_LIST = {
  all: BASE_API + "/api/v1/rule/search/all",
  addSearchRule: BASE_API + "/api/v1/rule/search/new",
  deleteSearchRule: BASE_API + "/api/v1/rule/search/delete",
  changeSearchRuleStatus: BASE_API + "/api/v1/rule/search/change_status",
  getDetail: BASE_API + "/api/v1/rule/search/get_detail",
  updateSearchRule: BASE_API + "/api/v1/rule/search/update"
};


const services = {

  all(context) {
    return context.axios.get(API_LIST.all);
  },

  addSearchRule(context, data) {
    return context.axios.post(API_LIST.addSearchRule, data, {withCredentials: true});
  },

  deleteSearchRule(context, data) {
    return context.axios.post(API_LIST.deleteSearchRule, data);
  },

  // 修改某个search rule 的状态
  changeStatus(context, data) {
    return context.axios.post(API_LIST.changeSearchRuleStatus, data);
  },

  // 根据id 或 rule_name获取search rule的详细信息
  // 包括search rule的filter rule
  // data = {
  //  "id": 11, "rule_name": "qqq"
  // }
  // 优先使用id获取信息
  getDetail(context, data) {
    return context.axios.get(API_LIST.getDetail, {params: data});
  },

  updateSearchRule(context, data) {
    return context.axios.post(API_LIST.updateSearchRule, data);
  },

};

export default services
