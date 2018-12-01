"use strict";

import config from "@/config/index";

const BASE_API = config.BASE_API;
const API_LIST = {
  getSearchResults: BASE_API + "/api/v1/results/all",
  ignoreResult: BASE_API + "/api/v1/results/ignore",
  confirmResult: BASE_API + "/api/v1/results/confirm",
};


export default {
  getAllSearchResults(ctx, data) {
    return ctx.axios.get(API_LIST.getSearchResults, {params: data})
  },

  ignore(ctx, data) {
    return ctx.axios.post(API_LIST.ignoreResult, data);
  },

  confirm(ctx, data) {
    return ctx.axios.post(API_LIST.confirmResult, data);
  },

}
