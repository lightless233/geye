import config from "@/config";


const API = {
  getAllRules: config.BASE_API + "/api/v1/rule/global/all",
  addGlobalFilterRule: config.BASE_API + "/api/v1/rule/global/new",
  deleteGlobalFilterRule: config.BASE_API + "/api/v1/rule/global/delete",
  updateGlobalFilterRule: config.BASE_API + "/api/v1/rule/global/update",
  getDetail: config.BASE_API + "/api/v1/rule/global/detail",
  changeStatus: config.BASE_API + "/api/v1/rule/global/change_status"
};

export default {

  getAllRules(ctx) {
    return ctx.axios.get(API.getAllRules);
  },

  addGlobalFilterRule(ctx, data) {
    return ctx.axios.post(API.addGlobalFilterRule, data);
  },

  deleteGlobalFilterRule(ctx, data) {
    return ctx.axios.post(API.deleteGlobalFilterRule, data);
  },

  updateGlobalFilterRule(ctx, data) {
    return ctx.axios.post(API.updateGlobalFilterRule, data);
  },

  getDetail(ctx, data) {
    return ctx.axios.get(API.getDetail, {params: data});
  },

  changeStatus(ctx, data) {
    return ctx.axios.post(API.changeStatus, data);
  },

}
