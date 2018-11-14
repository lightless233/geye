<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars"></font-awesome-icon>
          搜索规则管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div align="right">
        <el-button type="primary" @click="newSearchRuleButton">新建规则</el-button>
      </div>
      <el-table :data="searchRules" style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="table-expand">
              <el-form-item label="规则内容："><span>{{ props.row.rule_content }}</span></el-form-item>
              <el-form-item label="优先级："><span>{{props.row.priority}}</span></el-form-item>
              <el-form-item label="刷新间隔："><span>{{props.row.delay}}</span></el-form-item>
              <el-form-item label="命中是否通知："><span>{{props.row.need_notification}}</span></el-form-item>
              <el-form-item label="命中是否clone："><span>{{props.row.clone}}</span></el-form-item>
              <el-form-item label="更新时间："><span>{{props.row.updated_time}}</span></el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="#" prop="id"></el-table-column>
        <el-table-column label="规则名称" prop="rule_name"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <el-tag type="success" v-if="scope.row.status === 1">开启</el-tag>
            <el-tag v-else-if="scope.row.status === 0" type="error">关闭</el-tag>
            <el-tag v-else>未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="上次搜索时间" prop="last_refresh_time"></el-table-column>
        <el-table-column label="操作" width="150px">
          <template slot-scope="scope">
            <el-button size="mini" type="primary">编辑</el-button>
            <el-button size="mini" type="danger" @click="deleteSearchRule(scope.row.id, scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>

</template>

<script>

  import ruleServices from "@/services/searchRule";
  import HttpConstant from "@/utils/constant";

  export default {
    name: "search-rule-management",
    data() {
      return {
        searchRules: []
      }
    },
    mounted() {
      ruleServices.all(this)
        .then(response => {
          let responseData = response.data;
          if (responseData.code === 1001) {
            this.searchRules = responseData.data;
          } else {
            this.searchRules = [];
            this.$message.error(responseData.message);
          }
        })
        .catch(error => {
          console.error("error:", error);
          this.$message.error(HttpConstant.error_500);
        })
    },
    methods: {
      newSearchRuleButton: function () {
        this.$router.push({"name": "new-search-rule"});
      },

      deleteSearchRule: function (id, tableIndex) {
        console.log("id:", id);
        // todo 弹窗二次确认!
        ruleServices.deleteSearchRule(this, {"id": id})
          .then(response => {
            if (response.data.code === 1001) {
              this.$message.success(response.data.message);
              this.searchRules.splice(tableIndex, 1);
            } else {
              this.$message.error(response.data.message);
            }
          })
          .catch(error => {
            console.log("error:", error);
            this.$message.error(HttpConstant.error_500);
          });
      }
    }
  }
</script>

<style scoped>
  .table-expand {
    font-size: 0;
  }
  /*这个CSS不知道为啥不生效*/
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
