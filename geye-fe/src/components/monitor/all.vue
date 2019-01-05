<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars"></font-awesome-icon> 监控规则管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- ./面包屑导航 -->

    <!-- 主容器 -->
    <div class="container">
      <!-- 表头按钮部分 -->
      <div>
        <el-button type="primary" size="small" round @click="handleOpenDialog('add', -1, -1)">新建监控规则</el-button>
      </div>
      <!-- 表格，展示所有的监控规则 -->
      <el-table>

      </el-table>
    </div>
    <!-- ./主容器 -->


    <!-- 新建、编辑监控规则的dialog -->
    <el-dialog :title="dialogAttrs.title" :visible.sync="dialogAttrs.show">
      <el-form label-width="100px" :model="dialogAttrs.form" :loading="dialogAttrs.loading">
        <el-form-item label="任务类型">
          <el-select v-model="dialogAttrs.form.taskType" value="1">
            <el-option label="repo"></el-option>
            <el-option label="org"></el-option>
            <el-option label="user"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary">{{dialogAttrs.confirmBtnText}}</el-button>
        <el-button type="danger">取 消</el-button>
      </div>
    </el-dialog>
    <!-- ./新建、编辑监控规则的dialog -->

  </div>
</template>

<script>
  export default {
    name: "monitor-rule-management",
    // data
    data() {
      return {
        dialogAttrs: {
          title: "默认标题",
          confirmBtnText: "默认按钮",
          show: false,
          loading: false,
          type: "unknown",
          form: {
            taskType: null,
            eventType: null,
            ruleContent: null,
            status: null,
            interval: null,
            lastFetchTime: null,
            priority: null,
          }
        },

      }
    },
    // all methods
    methods: {
      clearForm: function() {

      },
      handleOpenDialog: function (type, tableIdx, row) {
        if (type === "add") {
          // 新建监控规则
          this.dialogAttrs.title = "新建监控规则";
          this.dialogAttrs.confirmBtnText = "添 加";
          this.dialogAttrs.type = "add";
          this.clearForm();
          this.dialogAttrs.show = true;
        } else if (type === "edit") {
          // 修改监控规则
        } else {
          this.$message.error("操作错误!");
        }
      }
    }
  }
</script>

<style scoped>

</style>
