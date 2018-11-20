import config from "@/config";


const API_LIST = {
  addFilterRule: config.BASE_API + "/api/v1/rule/filter/new",
  deleteFilterRule: config.BASE_API + "/api/v1/rule/filter/delete",
  getDetail: config.BASE_API + "/api/v1/rule/filter/detail",
  updateFilterRule: config.BASE_API + "/api/v1/rule/filter/update",
};


const services = {
  addFilterRule(ctx, data) {
    return ctx.axios.post(API_LIST.addFilterRule, data);
  },

  deleteFilterRule(ctx, data) {
    return ctx.axios.post(API_LIST.deleteFilterRule, data);
  },

  getFilterRuleDetail(ctx, data) {
    return ctx.axios.get(API_LIST.getDetail, {params: data})
  },

  updateFilterRule(ctx, data) {
    return ctx.axios.post(API_LIST.updateFilterRule, data);
  }

};

export default services;
