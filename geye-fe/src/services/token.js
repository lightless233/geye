"use strict";

import config from "@/config/index";


const BASE_API = config.BASE_API;
const API_LIST = {
  getAllTokens: BASE_API + "/v1/token/all",
  addToken: BASE_API + "/v1/token/new",
  updateToken: BASE_API + "/v1/token/update",
  deleteToken: BASE_API + "/v1/token/update",
  changeTokenStatus: BASE_API + "/v1/token/change_status",
  getTokenDetail: BASE_API + "/v1/token/detail",
};


export default {

  getAllTokens(ctx) {
    return ctx.axios.get(API_LIST.getAllTokens);
  },

  addToken(ctx, data) {
    return ctx.axios.post(API_LIST.addToken);
  },

  updateToken(ctx, data) {
    return ctx.axios.post(API_LIST.updateToken);
  },

  deleteToken(ctx, data) {
    return ctx.axios.post(API_LIST.deleteToken);
  },

  changeTokenStatus(ctx, data) {
    return ctx.axios.post(API_LIST.changeTokenStatus);
  },

  getTokenDetail(ctx, data) {
    return ctx.axios.get(API_LIST.getTokenDetail);
  },

}

