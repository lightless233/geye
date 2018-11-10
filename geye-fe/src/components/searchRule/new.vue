<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars" fixed-width=""></font-awesome-icon> 搜索规则管理
        </el-breadcrumb-item>
        <el-breadcrumb-item>
           新建搜索规则
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="container">
      <el-form ref="form" :model="form" :rules="formValidateRules" label-width="100px">
        <el-form-item label="规则名称">
          <el-input v-model="form.ruleName"></el-input>
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}" v-model="form.ruleContent"></el-input>
        </el-form-item>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则状态">
              <el-select v-model="form.status" value="1" style="width: 100%">
                <el-option :value="1" label="开启"></el-option>
                <el-option :value="0" label="关闭"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="通知状态" >
              <el-select v-model="form.notification" value="0" style="width: 100%">
                <el-option :value="1" label="开启通知"></el-option>
                <el-option :value="0" label="关闭通知"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="命中clone">
              <el-select v-model="form.clone" value="0" style="width: 100%">
                <el-option :value="1" label="开启命中自动clone"></el-option>
                <el-option :value="0" label="关闭命中自动clone"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="8">
            <el-form-item label="搜索间隔">
              <el-input type="number" value="30" v-model.number="form.delay">
                <template slot="append">分钟</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优先级">
              <el-input type="number" value="5" v-model.number="form.priority">
                <template slot="append">1~10</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="默认过滤">
              <el-select v-model="form.defaultFilter" value="1" style="width: 100%;">
                <el-option :value="1" label="添加默认过滤规则"></el-option>
                <el-option :value="0" label="不添加默认过滤规则"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24" align="right">
            <el-button type="primary" @click="confirmBtn('form')">确认</el-button>
            <el-button type="primary" plain @click="backBtn">返回</el-button>
          </el-col>
        </el-row>

      </el-form>
    </div>

  </div>
</template>

<script>

  import ruleService from "@/services/searchRule";

  export default {
    name: "new-search-rule",
    mounted: function () {
      // todo: move this to global mounted function
      this.axios.get("http://192.168.62.129:8080/api/_csrf_token", {withCredentials: true})
        .then(function (response) {
          document.cookie = "x-csrf-token=" + response.data + "; path=/";
        })
    },
    data() {
      return {
        form: {
          ruleName: "",
          ruleContent: "",
          status: 1,
          notification: 0,
          clone: 0,
          defaultFilter: 0,
          delay: 30,
          priority: 5,
        },
        formValidateRules: {
          ruleName: [
            { required: true, message: "请输入规则名称", trigger: "blur" },
            { min: 1, message: "规则名称不能为空", trigger: 'blur' },
          ],
          ruleContent: [
            {required: true, message: "请输入规则内容", trigger: "blur"},
            { min: 1, message: '规则内容不能为空', trigger: 'blur' },
          ]
        },
      }
    },
    methods: {
      confirmBtn: function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            ruleService.addSearchRule(this, this.form);
          } else {
            return false;
          }
        })
      },
      backBtn: function () {
        window.history.length > 1 ? this.$router.go(-1) : this.$router.push("/rule/search/all")
      }
    }
  }
</script>

<style scoped>

</style>