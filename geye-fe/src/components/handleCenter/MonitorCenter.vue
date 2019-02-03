<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars"></font-awesome-icon>
          监控结果
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- ./面包屑导航 -->
    <el-table :data="tableAttrs.dataset" style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <pre>{{JSON.stringify(JSON.parse(props.row.content), null, 2)}}</pre>
        </template>
      </el-table-column>
      <el-table-column label="#" prop="id"></el-table-column>
      <el-table-column label="事件信息">
        <template slot-scope="scope">{{scope.row.event_type}}#{{scope.row.event_id}}</template>
      </el-table-column>

      <el-table-column label="ACTOR信息">
        <template slot-scope="scope">
          <a target="_blank" :href="scope.row.actor_url" class="clean-href">{{scope.row.actor_login}} /
            {{scope.row.actor_display_name}}</a>
        </template>
      </el-table-column>

      <el-table-column label="ORG信息">
        <template slot-scope="scope">
          <span v-if="scope.row.org_name">
            <a :href="scope.row.org_url" target="_blank" class="clean-href">{{scope.row.org_name}}</a>
          </span>
          <span v-else>NO ORG</span>
        </template>
      </el-table-column>

      <el-table-column label="REPO信息">
        <template slot-scope="scope">
          <a target="_blank" :href="scope.row.repo_url" class="clean-href">{{scope.row.repo_name}}</a>
        </template>
      </el-table-column>

      <el-table-column label="事件事件" prop="event_created_time"></el-table-column>

    </el-table>

  </div>
</template>

<script>

  import monitorCenterService from "@/services/handleCenter/monitorCenter"
  import ApiConstant from "@/utils/constant";

  export default {
    name: "MonitorCenter",
    data() {
      return {
        tableAttrs: {
          dataset: [],
          loading: false,
        }
      }
    },

    mounted() {
      this.tableAttrs.loading = true;
      monitorCenterService.getALlMonitorResult(this)
        .then(resp => {
          let code = resp.data.code;
          let message = resp.data.message;
          if (code === 1001) {
            this.tableAttrs.dataset = resp.data.data;
          } else {
            this.$message.error(message);
          }
        })
        .catch(err => {
          console.error(`error: ${err}`);
          this.message.error(ApiConstant.error_500);
        })
        .then(() => {
          this.tableAttrs.loading = false;
        })
    }
  }
</script>

<style scoped>
  .clean-href:hover, .clean-href:link, .clean-href:active, .clean-href {
    text-decoration: none;
    color: #303133;
  }
</style>
