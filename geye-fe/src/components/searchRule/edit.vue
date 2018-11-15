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

    <div class="container">
      <el-form ref="searchRuleForm" :model="searchRuleForm" label-width="100px" :disabled="isDisabled">
        <el-form-item label="规则名称">
          <el-input v-model="searchRuleForm.ruleName"></el-input>
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}" v-model="searchRuleForm.ruleContent"></el-input>
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
            <el-button type="primary" @click="confirmBtn">确认修改</el-button>
            <el-button type="primary" plain @click="backBtn">返回规则列表</el-button>
          </el-col>
        </el-row>

      </el-form>
    </div>

    <!-- 展示filter rule的表格部分-->
    <div class="container" style="margin-top: 20px">

    </div>

  </div>
</template>

<script>

  import searchRuleService from "@/services/searchRule";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "edit-search-rule",
    data() {
      return {
        searchRuleForm: {
          ruleName: "",
          ruleContent: "",
          status: 1,
          needNotification: 0,
          clone: 0,
          delay: 30,
          priority: 5,
        },
        isDisabled: false,
      }
    },
    mounted: function (){
      searchRuleService.getDetail(this, {"id": this.$route.params.srid})
        .then(response => {
          let responseData = response.data;
          if (responseData.code === 1001) {
            this.searchRuleForm = responseData.data.search_rule
          }
        })
        .catch(error => {
          console.error("error:", error);
          this.isDisabled = true;
          this.$message.error(ApiConstant.error_500);
        })
    },
    methods: {
      goSearchRuleList: function () {
        this.$router.push({"name": "all-search-rule"})
      },

      backBtn: function () {
        window.history.length > 1 ? this.$router.go(-1) : this.$router.push({"name": "all-search-rule"})
      },

      confirmBtn: function () {

      }
    }
  }
</script>
