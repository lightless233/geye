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
      <el-table
          :data="searchRules"
          style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="table-expand">
              <el-form-item label="商品名称">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="所属店铺">
                <span>{{ props.row.shop }}</span>
              </el-form-item>
              <el-form-item label="商品 ID">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="店铺 ID">
                <span>{{ props.row.shopId }}</span>
              </el-form-item>
              <el-form-item label="商品分类">
                <span>{{ props.row.category }}</span>
              </el-form-item>
              <el-form-item label="店铺地址">
                <span>{{ props.row.address }}</span>
              </el-form-item>
              <el-form-item label="商品描述">
                <span>{{ props.row.desc }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
            label="#"
            prop="id">
        </el-table-column>
        <el-table-column
            label="商品名称"
            prop="name">
        </el-table-column>
        <el-table-column
            label="描述"
            prop="desc">
        </el-table-column>
      </el-table>
    </div>
  </div>

</template>

<script>

  // import config from "@/config";
  import ruleServices from "@/services/searchRule";

  export default {
    name: "search-rule-management",
    data() {
      return {
        tableData5: [],
        searchRules: null
      }
    },
    mounted() {
      ruleServices.all(this)
        .then(response => (this.searchRules = response.data))
    },
    methods: {
      newSearchRuleButton: function () {
        this.$router.push({"name": "new-search-rule"});
      }
    }
  }
</script>

<style scoped>
  .table-expand {
    font-size: 0;
  }

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
