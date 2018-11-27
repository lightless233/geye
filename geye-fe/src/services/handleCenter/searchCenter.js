"use strict";

import config from "@/config/index";

const BASE_API = config.BASE_API;
const API_LIST = {
  getSearchResults: BASE_API + "/api/v1/results/all",
};


export default {
  getAllSearchResults(ctx, data) {
    return ctx.axios.get(API_LIST.getSearchResults, {params: data})
  },
}
