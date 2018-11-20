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
            <el-button type="primary" size="small" round>新建全局过滤规则</el-button>
          </div>
        </el-col>
      </el-row>

      <!-- table start -->
      <el-table style="width: 100%" v-loading="loading" :data="globalFilterRules">
        <!-- 展开的内容 -->
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline>
              <el-form-item label="规则内容" label-width="100px">
                <span>{{ props.row.ruleContent }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="#"></el-table-column>
        <el-table-column label="规则名称"></el-table-column>
        <el-table-column label="状态"></el-table-column>
        <el-table-column label="规则类型"></el-table-column>
        <el-table-column label="规则引擎"></el-table-column>
        <el-table-column label="生效位置"></el-table-column>
        <el-table-column label="命中操作"></el-table-column>
        <el-table-column slot-scope="scope">
          <el-button size="mini" type="primary">编辑</el-button>
          <el-button size="mini" type="danger">删除</el-button>
        </el-table-column>
      </el-table>
      <!-- ./table end -->
    </div>

    <!-- 新建/编辑 dialog -->
    <el-dialog :title="dialogTitle" :visible.sync="showRuleDialog">
      <el-form :model="globalRuleForm" label-width="100px" :disabled="isDisableForm">
        <el-row>
          <el-form-item></el-form-item>
        </el-row>

        <el-row>
          <el-form-item></el-form-item>
        </el-row>

        <el-row>
          <el-col :span="8"></el-col>
          <el-col :span="8"></el-col>
          <el-col :span="8"></el-col>
        </el-row>

        <el-row>
          <el-col :span="8"></el-col>
          <el-col :span="8"></el-col>
          <el-col :span="8"></el-col>
        </el-row>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button type="primary"> {{dialogConfirmButtonText}} </el-button>
        <el-button type="danger">关闭</el-button>
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
        globalRuleForm: {}
      };
    },

    mounted() {
      this.loading = true;
      globalRuleService.getAllRules(this)
        .then(resp => {
          if (resp.data.code === 1001) {
            this.globalFilterRules = resp.data.data;
          } else {
            this.$message.error(resp.data.message);
          }
        })
        .catch(e => {
          this.$message.error(ApiConstant.error_500);
          console.log("error: ", e);
        })
        .then(_ => {
          this.loading = false;
        });
    },

  }
</script>

<style scoped>

</style>
