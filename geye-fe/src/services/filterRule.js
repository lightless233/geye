import config from "@/config";


const API_LIST = {
  addFilterRule: config.BASE_API + "/api/v1/rule/filter/new",
};


const services = {
  addFilterRule(ctx, data) {
    return ctx.axios.post(API_LIST.addFilterRule, data);
  }
};

export default services;
