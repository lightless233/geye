"use strict";

import config from "@/config/index";

const BASE_API = config.BASE_API;
const BASE_PATH = `${BASE_API}/api/v1/results/monitor`;
const API_LIST = {
    all: `${BASE_PATH}/all`,
};

export default {
    getALlMonitorResult(context) {
        return context.axios.get(API_LIST.all);
    }
}