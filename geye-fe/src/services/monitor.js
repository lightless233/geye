"use strict";

import config from "@/config/index";

const BASE_API = config.BASE_API;
const BASE_PATH = `${BASE_API}/api/v1/rule/monitor`;
const API_LIST = {
  add: `${BASE_PATH}/new`,
  update: `${BASE_PATH}/update`,
  delete: `${BASE_PATH}/delete`,
  all: `${BASE_PATH}/all`,
};

export default {

  addMonitorRule(context, data) {
    return context.axios.post(API_LIST.add, data);
  },

  updateMonitorRule(context, data) {
    return context.axios.post(API_LIST.update, data);
  },

  deleteMonitorRule(context, id) {
    return context.axios.post(API_LIST.delete, {id: id});
  },

  getAllMonitorRule(context) {
    return context.axios.get(API_LIST.all);
  }

}
