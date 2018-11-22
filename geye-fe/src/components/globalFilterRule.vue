<template>
  <div>
    <!-- 导航 -->
    <div class="crumbs" style="margin-bottom: 30px">
      <el-breadcrumb separator="|">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars"></font-awesome-icon>
          全局过滤规则管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- main container -->
    <div class="container">
      <el-row>
        <el-col :span="12"><h4>全局过滤规则管理</h4></el-col>
        <el-col :span="12">
          <div align="right">
            <el-button type="primary" size="small" round @click="openDialog('new', -1, -1)">新建全局过滤规则</el-button>
          </div>
        </el-col>
      </el-row>

      <!-- table start -->
      <el-table :data="globalFilterRules" style="width: 100%" v-loading="loading">
        <!-- 展开的内容 -->
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline label-width="100px">
              <el-form-item label="规则内容">
                <span>{{ props.row.ruleContent }}</span>
              </el-form-item>
              <br>
              <el-form-item label="优先级">
                <span>{{props.row.priority}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="#" prop="id"></el-table-column>
        <el-table-column label="规则名称" prop="name"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 1" type="success">开启</el-tag>
            <el-tag v-else-if="scope.row.status === 0" type="danger">关闭</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="规则类型">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.ruleType === 1" type="primary">正向匹配</el-tag>
            <el-tag v-else-if="scope.row.ruleType === 2" type="primary">反向匹配</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="引擎类型">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.ruleEngine === 1" type="primary">正则引擎</el-tag>
            <el-tag v-else-if="scope.row.ruleEngine === 2" type="primary">串匹配引擎</el-tag>
            <el-tag v-else>未知引擎</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="过滤位置">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.position === 1">作者</el-tag>
            <el-tag v-else-if="scope.row.position === 2">仓库名</el-tag>
            <el-tag v-else-if="scope.row.position === 3">文件路径</el-tag>
            <el-tag v-else-if="scope.row.position === 4">代码内容</el-tag>
            <el-tag v-else-if="scope.row.position === 5">文件名</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="命中操作">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.action === 1">继续匹配下一条规则</el-tag>
            <el-tag v-else-if="scope.row.action === 2">设为误报-不保存</el-tag>
            <el-tag v-else-if="scope.row.action === 3">设为误报-保存</el-tag>
            <el-tag v-else-if="scope.row.action === 4">设为确认-保存</el-tag>
            <el-tag v-else-if="scope.row.action === 5">设为待确认-保存</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column>
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="openDialog('edit', scope.row.id, scope.$index)">编辑</el-button>
            <el-button size="mini" type="danger" @click="deleteRuleFn(scope.row.id, scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- ./table end -->
    </div>

    <!-- 新建/编辑 dialog -->
    <el-dialog :title="dialogTitle" :visible.sync="showRuleDialog">
      <el-form :model="globalRuleForm" label-width="100px" :disabled="isDisableForm">
        <el-row>
          <el-form-item label="规则名称">
            <el-input v-model="ruleForm.name" autocomplete="off"></el-input>
          </el-form-item>
        </el-row>

        <el-row>
          <el-form-item label="规则内容">
            <el-input v-model="ruleForm.ruleContent" type="textarea" :autosize="{minRows: 3, maxRows: 3}"></el-input>
          </el-form-item>
        </el-row>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则引擎">
              <el-select v-model="ruleForm.ruleEngine" :value="2" style="width: 100%">
                <el-option label="正则引擎" :value="1"></el-option>
                <el-option label="串匹配引擎" :value="2"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优先级">
              <el-input v-model="ruleForm.priority" autocomplete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="ruleForm.status" :value="1" style="width: 100%;">
                <el-option label="开启" :value="1"></el-option>
                <el-option label="关闭" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则类型">
              <el-select v-model="ruleForm.ruleType" :value="1" style="width: 100%;">
                <el-option label="正向匹配" :value="1"/>
                <el-option label="反向匹配" :value="2"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="匹配位置">
              <el-select v-model="ruleForm.position" :value="4" style="width: 100%;">
                <el-option label="仓库作者" :value="1"/>
                <el-option label="仓库名称" :value="2"/>
                <el-option label="文件路径" :value="3"/>
                <el-option label="代码内容" :value="4"/>
                <el-option label="文件名" :value="5"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="命中操作">
              <el-select v-model="ruleForm.action" :value="5" style="width: 100%;">
                <el-option label="继续匹配下一条规则" :value="1"/>
                <el-option label="设为误报-不保存" :value="2"/>
                <el-option label="设为误报-保存" :value="3"/>
                <el-option label="设为确认-保存" :value="4"/>
                <el-option label="设为待确认-保存" :value="5"/>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogConfirmButton"> {{dialogConfirmButtonText}}</el-button>
        <el-button type="danger" @click="showRuleDialog = false">关闭</el-button>
      </div>

    </el-dialog>

  </div>
</template>

<script>

  import globalRuleService from "@/services/globalFilterRule";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "globalFilterRule",

    data() {
      return {
        loading: false,
        globalFilterRules: [],

        // dialog相关的变量
        dialogTitle: "新建全局过滤规则",
        dialogConfirmButtonText: "确认",
        showRuleDialog: false,
        isDisableForm: false,
        globalRuleForm: {},
        editingRuleId: -1,
        editingTableIdx: -1,
        dialogType: "new",

        // 表单变量
        ruleForm: {
          id: 0,
          name: "",
          ruleType: 1,
          ruleEngine: 2,
          ruleContent: "",
          status: 1,
          action: 5,
          position: 4,
          priority: 5,
        }
      };
    },

    mounted() {
      this.loading = true;
      globalRuleService.getAllRules(this)
        .then(resp => {
          if (resp.data.code === 1001) {
            this.globalFilterRules = resp.data.data;
            // console.log(this.globalFilterRules);
          } else {
            this.$message.error(resp.data.message);
          }
        })
        .catch(e => {
          this.$message.error(ApiConstant.error_500);
          console.log("error: ", e);
        })
        .then(() => {
          this.loading = false;
        });
    },

    methods: {

      initForm: function () {
        this.ruleForm.id = 0;
        this.ruleForm.name = "";
        this.ruleForm.ruleType = 1;
        this.ruleForm.ruleEngine = 2;
        this.ruleForm.ruleContent = "";
        this.ruleForm.status = 1;
        this.ruleForm.action = 5;
        this.ruleForm.position = 4;
        this.ruleForm.priority = 5;
      },

      openDialog: function (type, globalRuleId, tableIdx) {
        this.initForm();
        this.isDisableForm = false;
        if (type === "new") {
          this.dialogType = "new";
          this.dialogTitle = "新建全局过滤规则";
          this.dialogConfirmButtonText = "添加";
          this.showRuleDialog = true;
        } else if (type === "edit") {
          this.dialogType = "edit";
          this.dialogTitle = "编辑全局过滤规则";
          this.dialogConfirmButtonText = "更新";
          this.editingRuleId = globalRuleId;
          this.editingTableIdx = tableIdx;
          // request for detail
          globalRuleService.getDetail(this, {"id": globalRuleId})
            .then(resp => {
              if (resp.data.code === 1001) {
                this.showRuleDialog = true;
                let data = resp.data.data;
                this.ruleForm.id = data.id;
                this.ruleForm.name = data.name;
                this.ruleForm.ruleType = data.ruleType;
                this.ruleForm.ruleEngine = data.ruleEngine;
                this.ruleForm.ruleContent = data.ruleContent;
                this.ruleForm.status = data.status;
                this.ruleForm.action = data.action;
                this.ruleForm.position = data.position;
                this.ruleForm.priority = data.priority;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(err => {
              this.$message.error(ApiConstant.error_500);
              console.log("error:", err);
              this.isDisableForm = true;
            });
        }
      },

      dialogConfirmButton: function () {
        if (this.dialogType === "new") {
          globalRuleService.addGlobalFilterRule(this, this.ruleForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                this.showRuleDialog = false;
                this.globalFilterRules.push(resp.data.data);
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(e => {
              console.log("error:", e);
              this.$message.error(ApiConstant.error_500);
            });
        } else if (this.dialogType === "edit") {
          globalRuleService.updateGlobalFilterRule(this, this.ruleForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                let data = resp.data.data;
                this.globalFilterRules[this.editingTableIdx].id = data.id;
                this.globalFilterRules[this.editingTableIdx].name = data.name;
                this.globalFilterRules[this.editingTableIdx].ruleType = data.ruleType;
                this.globalFilterRules[this.editingTableIdx].ruleEngine = data.ruleEngine;
                this.globalFilterRules[this.editingTableIdx].ruleContent = data.ruleContent;
                this.globalFilterRules[this.editingTableIdx].status = data.status;
                this.globalFilterRules[this.editingTableIdx].action = data.action;
                this.globalFilterRules[this.editingTableIdx].position = data.position;
                this.globalFilterRules[this.editingTableIdx].priority = data.priority;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(e => {
              console.log("error:", e);
              this.$message.error(ApiConstant.error_500);
            });
        }
      },

      deleteRuleFn: function (frid, tableIdx) {
        globalRuleService.deleteGlobalFilterRule(this, {"id": frid})
          .then(resp => {
            if (resp.data.code === 1001) {
              this.$message.success(resp.data.message);
              this.globalFilterRules.splice(tableIdx, 1);
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.log("error:", err)
          });
      }

    }
  }
</script>

<style scoped>

</style>
