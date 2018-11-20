<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item @click.native="goSearchRuleList" style="cursor: pointer;">
          <font-awesome-icon icon="bars" fixed-width=""></font-awesome-icon>
          搜索规则管理
        </el-breadcrumb-item>
        <el-breadcrumb-item>
          编辑搜索规则
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="container" v-loading="loading">
      <el-form ref="searchRuleForm" :model="searchRuleForm" label-width="100px" :disabled="isDisabled">
        <el-form-item label="规则名称">
          <el-input v-model="searchRuleForm.ruleName"></el-input>
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}"
                    v-model="searchRuleForm.ruleContent"></el-input>
        </el-form-item>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则状态">
              <el-select v-model="searchRuleForm.status" value="1" style="width: 100%">
                <el-option :value="1" label="开启"></el-option>
                <el-option :value="0" label="关闭"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="通知状态">
              <el-select v-model="searchRuleForm.needNotification" value="0" style="width: 100%">
                <el-option :value="1" label="开启通知"></el-option>
                <el-option :value="0" label="关闭通知"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="命中clone">
              <el-select v-model="searchRuleForm.clone" value="0" style="width: 100%">
                <el-option :value="1" label="开启命中自动clone"></el-option>
                <el-option :value="0" label="关闭命中自动clone"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="搜索间隔">
              <el-input type="number" value="30" v-model.number="searchRuleForm.delay">
                <template slot="append">分钟</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级">
              <el-input type="number" value="5" v-model.number="searchRuleForm.priority">
                <template slot="append">1~10</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24" align="right">
            <el-button type="primary" @click="updateSearchRuleButton">确认修改</el-button>
            <el-button type="primary" plain @click="backBtn">返回规则列表</el-button>
          </el-col>
        </el-row>

      </el-form>
    </div>

    <!-- 展示filter rule的表格部分-->
    <div class="container" style="margin-top: 20px" v-loading="loading">
      <el-row>
        <el-col :span="12">
          <h4>过滤规则列表</h4>
        </el-col>
        <el-col :span="12" align="right">
          <div align="right">
            <el-button type="primary" @click="openFilterRuleDialog('new', -1, -1)" size="small" round>新建过滤规则</el-button>
          </div>
        </el-col>
      </el-row>
      <el-table :data="filterRuleList" style="width: 100%">
        <el-table-column prop="id" label="#" width="60px"></el-table-column>
        <el-table-column prop="name" label="规则名称"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 1" type="success">开启</el-tag>
            <el-tag v-else-if="scope.row.status === 0" type="danger">关闭</el-tag>
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
        <el-table-column label="规则类型">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.ruleType === 1" type="primary">正向匹配</el-tag>
            <el-tag v-else-if="scope.row.ruleType === 2" type="primary">反向匹配</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="规则效果">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.action === 1">继续匹配下一条规则</el-tag>
            <el-tag v-else-if="scope.row.action === 2">设为误报-不保存</el-tag>
            <el-tag v-else-if="scope.row.action === 3">设为误报-保存</el-tag>
            <el-tag v-else-if="scope.row.action === 4">设为确认-保存</el-tag>
            <el-tag v-else-if="scope.row.action === 5">设为待确认-保存</el-tag>
            <el-tag v-else>未知</el-tag>
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
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="openFilterRuleDialog('edit', scope.row.id, scope.$index)">编辑
            </el-button>
            <el-button size="mini" type="danger" @click="deleteFilterRule(scope.row.id, scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑 过滤规则的对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="showFilterRuleDialog" :fullscreen="true">
      <el-form :model="filterRuleForm" label-width="100px" :disabled="isDisableFilterRuleForm">
        <el-form-item label="规则标题">
          <el-input v-model="filterRuleForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}" v-model="filterRuleForm.ruleContent"/>
        </el-form-item>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则引擎">
              <el-select v-model="filterRuleForm.ruleEngine" :value="2" style="width: 100%;">
                <el-option label="正则引擎" :value="1"></el-option>
                <el-option label="串匹配引擎" :value="2"></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="优先级">
              <el-input v-model="filterRuleForm.priority" autocomplete="off" type="number"/>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="filterRuleForm.status" :value="1" style="width: 100%;">
                <el-option label="开启" :value="1"></el-option>
                <el-option label="关闭" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="8">
            <!--rule type-->
            <el-form-item label="规则类型">
              <el-select v-model="filterRuleForm.ruleType" :value="1" style="width: 100%;">
                <el-option label="正向匹配" :value="1"/>
                <el-option label="反向匹配" :value="2"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <!--position-->
            <el-form-item label="匹配位置">
              <el-select v-model="filterRuleForm.position" :value="4" style="width: 100%;">
                <el-option label="仓库作者" :value="1"/>
                <el-option label="仓库名称" :value="2"/>
                <el-option label="文件路径" :value="3"/>
                <el-option label="代码内容" :value="4"/>
                <el-option label="文件名" :value="5"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <!--action-->
            <el-form-item label="命中操作">
              <el-select v-model="filterRuleForm.action" :value="5" style="width: 100%;">
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
        <el-button type="primary" @click="confirmFilterRuleButton">{{dialogConfirmBtnText}}</el-button>
        <el-button type="danger" @click="showFilterRuleDialog = false">关 闭</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

  import searchRuleService from "@/services/searchRule";
  import filterRuleService from "@/services/filterRule";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "edit-search-rule",
    data() {
      return {
        loading: false,
        searchRuleForm: {
          id: this.$route.params.srid,
          ruleName: "",
          ruleContent: "",
          status: 1,
          needNotification: 0,
          clone: 0,
          delay: 30,
          priority: 5,
        },
        isDisabled: false,
        filterRuleList: [],

        showFilterRuleDialog: false,
        isDisableFilterRuleForm: false,
        dialogTitle: "新建过滤规则",
        dialogConfirmBtnText: "添 加",
        editingFilterRuleId: -1,
        lastTableIndex: -1,
        dialogType: "",
        filterRuleForm: {
          name: "",
          ruleType: 1,
          ruleEngine: 2,
          ruleContent: "",
          status: 1,
          action: 5,
          position: 4,
          priority: 5,
        }
      }
    },
    mounted: function () {
      this.loading = true;
      searchRuleService.getDetail(this, {"id": this.$route.params.srid})
        .then(response => {
          let responseData = response.data;
          if (responseData.code === 1001) {
            this.searchRuleForm = responseData.data.search_rule;
            this.filterRuleList = responseData.data.filter_rule;
          }
        })
        .catch(error => {
          console.error("error:", error);
          this.isDisabled = true;
          this.$message.error(ApiConstant.error_500);
        })
        .then(_ => {
          this.loading = false;
        })
    },
    methods: {
      goSearchRuleList: function () {
        this.$router.push({"name": "all-search-rule"})
      },

      backBtn: function () {
        window.history.length > 1 ? this.$router.go(-1) : this.$router.push({"name": "all-search-rule"})
      },

      updateSearchRuleButton: function () {
        this.searchRuleForm.id = this.$route.params.srid;
        console.log("searchRuleForm:", this.searchRuleForm);
        searchRuleService.updateSearchRule(this, this.searchRuleForm)
          .then(response => {
            let d = response.data;
            if (d.code === 1001) {
              this.$message.success(d.message);
            } else {
              this.$message.error(d.message);
            }
          })
          .catch(error => {
            this.$message.error(ApiConstant.error_500);
            console.error("error:", error);
          })
      },

      openFilterRuleDialog: function (type, id, tableIdx) {
        this.dialogType = type;
        this.editingFilterRuleId = id;
        this.lastTableIndex = tableIdx;
        if (this.dialogType === "new") {
          // 新建过滤规则的dialog
          this.dialogTitle = "新建过滤规则";
          this.dialogConfirmBtnText = "添 加";
          this.initFilterRuleForm();
          this.showFilterRuleDialog = true;
        } else if (this.dialogType === "edit") {
          // 编辑filter rule，先获取要编辑的规则内容，并且填充表单
          filterRuleService.getFilterRuleDetail(this, {"id": this.editingFilterRuleId})
            .then(response => {
              // 加载成功，设置内容
              if (response.data.code === 1001) {
                let data = response.data.data;
                this.dialogTitle = "编辑过滤规则";
                this.dialogConfirmBtnText = "更 新";
                this.filterRuleForm = {
                  name: data.name,
                  ruleType: data.ruleType,
                  ruleEngine: data.ruleEngine,
                  ruleContent: data.ruleContent,
                  status: data.status,
                  action: data.action,
                  position: data.position,
                  priority: data.priority,
                };
                // 打开dialog
                this.showFilterRuleDialog = true;
              } else {
                this.$message.error(response.data.message);
              }
            })
            .catch(err => {
              // 获取待编辑的filter rule的详细信息失败了
              console.log("error: ", err);
              this.$message.error(ApiConstant.error_500);
            });

        }
      },

      confirmFilterRuleButton: function () {
        if (this.dialogType === "new") {
          this.filterRuleForm.id = this.$route.params.srid;
          filterRuleService.addFilterRule(this, this.filterRuleForm)
            .then(response => {
              if (response.data.code === 1001) {
                this.$message.success(response.data.message);
                this.showFilterRuleDialog = false;
                this.filterRuleList.push(response.data.data);
              } else {
                this.$message.error(response.data.message);
              }
            })
            .catch(err => {
              console.error("error:", err);
              this.$message.error(ApiConstant.error_500);
            });
        } else if (this.dialogType === "edit") {
          this.filterRuleForm.id = this.editingFilterRuleId;
          filterRuleService.updateFilterRule(this, this.filterRuleForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                // 根据tableIndex更新表格中展示的内容
                this.filterRuleList[this.lastTableIndex]["name"] = this.filterRuleForm["name"];
                this.filterRuleList[this.lastTableIndex]["status"] = this.filterRuleForm["status"];
                this.filterRuleList[this.lastTableIndex]["ruleEngine"] = this.filterRuleForm["ruleEngine"];
                this.filterRuleList[this.lastTableIndex]["ruleType"] = this.filterRuleForm["ruleType"];
                this.filterRuleList[this.lastTableIndex]["action"] = this.filterRuleForm["action"];
                this.filterRuleList[this.lastTableIndex]["position"] = this.filterRuleForm["position"];
              } else {
                this.$message.error(resp.data.message);
              }
            })
        }
      },

      initFilterRuleForm: function () {
        this.filterRuleForm = {
          name: "",
          ruleType: 1,
          ruleEngine: 2,
          ruleContent: "",
          status: 1,
          action: 5,
          position: 4,
          priority: 5,
        }
      },

      deleteFilterRule: function (id, tableIndex) {
        filterRuleService.deleteFilterRule(this, {"id": id})
          .then(response => {
            if (response.data.code === 1001) {
              this.$message.success(response.data.message);
              this.filterRuleList.splice(tableIndex, 1);
            } else {
              this.$message.error(response.data.message);
            }
          })
          .catch(err => {
            console.error("error:", err);
            this.$message.error(ApiConstant.error_500);
          });
      }
    }
  }
</script>
