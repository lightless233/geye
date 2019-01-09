<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars"></font-awesome-icon>
          监控规则管理
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
      <el-table :data="tableAttrs.dataset" style="width: 100%" v-loading="tableAttrs.loading">
        <el-table-column prop="id" label="#" width="100px"></el-table-column>
        <el-table-column label="任务类型" width="150px">
          <template slot-scope="scope">{{convertTaskType(scope.row.taskType)}}</template>
        </el-table-column>
        <el-table-column label="事件类型" width="150px">
          <template slot-scope="scope">{{convertEventType(scope.row.eventType)}}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100px">
          <template slot-scope="scope">
            <el-tag type="danger" v-if="!scope.row.status" style="cursor: pointer">关闭</el-tag>
            <el-tag type="success" v-else-if="scope.row.status" style="cursor: pointer">开启</el-tag>
            <el-tag v-else style="cursor: pointer">未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ruleContent" label="监控内容" align="center"></el-table-column>
        <el-table-column label="操作" width="150px">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" round @click="handleOpenDialog('update', scope.$index, scope.row)">
              编辑
            </el-button>
            <el-button size="mini" type="danger" round @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- ./主容器 -->


    <!-- 新建、编辑监控规则的dialog -->
    <el-dialog :title="dialogAttrs.title" :visible.sync="dialogAttrs.show">
      <el-form label-width="100px" :model="dialogAttrs.form" v-loading="dialogAttrs.loading">
        <el-row>
          <el-col :span="12">
            <el-form-item label="任务类型">
              <el-select v-model="dialogAttrs.form.taskType" :value="dialogAttrs.form.taskType" style="width: 100%">
                <el-option value="repo" label="仓库"></el-option>
                <el-option value="org" label="组织"></el-option>
                <el-option value="user" label="用户"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事件类型">
              <el-select v-model="dialogAttrs.form.eventType" :value="dialogAttrs.form.eventType" style="width: 100%">
                <el-option value="push_event" label="PushEvent"></el-option>
                <el-option value="release_event" label="ReleaseEvent"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="监控内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}"
                    v-model="dialogAttrs.form.ruleContent"></el-input>
          <div>
            规则样例:<br>
            1. 组织监控：{"org_name": ""}<br>
            2. 仓库监控：{"owner": "", "repo_name": ""}<br>
            3. 用户监控：{"username": ""}
          </div>
        </el-form-item>

        <el-row>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="dialogAttrs.form.status" :value="1" style="width: 100%">
                <el-option :value="1" label="开启"></el-option>
                <el-option :value="0" label="关闭"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="刷新间隔">
              <el-input v-model="dialogAttrs.form.interval" style="width: 100%"
                        autocomplete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优先级(分钟)">
              <el-input v-model="dialogAttrs.form.priority" style="width: 100%"
                        autocomplete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <!--dialog footer-->
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleConfirm">{{dialogAttrs.confirmBtnText}}</el-button>
        <el-button type="danger" @click="handleCancel">取 消</el-button>
      </div>
    </el-dialog>
    <!-- ./新建、编辑监控规则的dialog -->

  </div>
</template>

<script>

  import sMonitorRule from "@/services/monitor";
  import ApiConstant from "@/utils/constant";

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
          type: "unknown", // add, update
          form: {
            id: null,
            taskType: null,
            eventType: null,
            ruleContent: null,
            status: 1,
            interval: 5,
            priority: 5,
          },
          currentTableIdx: null,
        },
        tableAttrs: {
          dataset: [],
          loading: false,
        },
      }
    },
    computed: {},
    // 加载页面时读取所有的规则
    mounted() {
      this.tableAttrs.loading = true;
      sMonitorRule.getAllMonitorRule(this)
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
          this.$message.error(ApiConstant.error_500);
        })
        .then(() => {
          this.tableAttrs.loading = false;
        })
    },
    // all methods
    methods: {
      convertTaskType: function (val) {
        if (val === "repo") {
          return "仓库监控";
        } else if (val === "user") {
          return "用户监控";
        } else if (val === "org") {
          return "组织监控";
        } else {
          return "未知";
        }
      },

      convertEventType: function (val) {
        if (val === "push_event") {
          return "PushEvent";
        } else if (val === "release_event") {
          return "ReleaseEvent";
        } else {
          return "未知";
        }
      },
      clearForm: function () {
        this.dialogAttrs.form.taskType = null;
        this.dialogAttrs.form.eventType = null;
        this.dialogAttrs.form.ruleContent = null;
        this.dialogAttrs.form.status = 1;
        this.dialogAttrs.form.interval = 5;
        this.dialogAttrs.form.priority = 5;
        this.dialogAttrs.form.id = null;
      },
      handleOpenDialog: function (type, tableIdx, row) {
        if (type === "add") {
          // 新建监控规则
          this.dialogAttrs.title = "新建监控规则";
          this.dialogAttrs.confirmBtnText = "添 加";
          this.dialogAttrs.type = "add";
          this.clearForm();
          this.dialogAttrs.show = true;
        } else if (type === "update") {
          // 修改监控规则
          this.dialogAttrs.title = "编辑监控规则";
          this.dialogAttrs.confirmBtnText = "更 新";
          this.dialogAttrs.type = "update";
          this.dialogAttrs.currentTableIdx = tableIdx;
          this.dialogAttrs.show = true;

          this.dialogAttrs.form.eventType = row.eventType;
          this.dialogAttrs.form.taskType = row.taskType;
          this.dialogAttrs.form.priority = row.priority;
          this.dialogAttrs.form.interval = row.interval;
          this.dialogAttrs.form.status = Number(row.status);
          this.dialogAttrs.form.ruleContent = row.ruleContent;
          this.dialogAttrs.form.id = row.id;
        } else {
          this.$message.error("操作错误!");
        }
      },

      handleCancel: function () {
        // 关闭dialog
        this.dialogAttrs.show = false;
      },

      handleConfirm: function () {
        // 处理dialog，根据不同的type，调用不同的service
        // console.log(this.dialogAttrs.form);
        let confirmType = this.dialogAttrs.type;
        // console.log(`confirmType: ${confirmType}`);

        this.dialogAttrs.loading = true;

        let reqPromise = null;
        if (confirmType === "add") {
          reqPromise = sMonitorRule.addMonitorRule(this, this.dialogAttrs.form);
        } else if (confirmType === "update") {
          reqPromise = sMonitorRule.updateMonitorRule(this, this.dialogAttrs.form);
        } else {
          this.$message.error("操作错误!");
        }

        // 处理返回结果
        reqPromise
          .then(resp => {
            let code = resp.data.code;
            let msg = resp.data.message;
            if (code === 1001) {
              this.$message.success(msg);

              if (confirmType === "add") {
                this.tableAttrs.dataset.push(resp.data.data);
                this.dialogAttrs.show = false;
                this.clearForm();

              } else if (confirmType === "update") {
                // 更新表格中对应的数据
                let row = this.tableAttrs.dataset[this.dialogAttrs.currentTableIdx];
                let form = this.dialogAttrs.form;

                let keys = ["taskType", "eventType", "status", "priority", "ruleContent", "interval"];
                for (const key of keys) {
                  row[key] = form[key];
                }
              }

            } else {
              this.$message.error(msg);
            }
          })
          .catch(err => {
            console.error("error:", err);
            this.$message.error(ApiConstant.error_500);
          })
          .then(() => {
            this.dialogAttrs.loading = false;
          });
      },

      handleDelete: function (idx, row) {
        this.tableAttrs.loading = true;
        let id = row.id;
        sMonitorRule.deleteMonitorRule(this, id)
          .then(resp => {
            let code = resp.data.code;
            let message = resp.data.message;
            if (code === 1001) {
              this.tableAttrs.dataset.splice(idx, 1);
              this.$message.success(message);
            } else {
              this.$message.error(message);
            }
          })
          .catch(err => {
            console.error(`error: ${err}`);
            this.$message.error(ApiConstant.error_500);
          })
          .then(() => {
            this.tableAttrs.loading = false;
          })
      }
    }
  }
</script>

<style scoped>

</style>
