<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars" fixed-width></font-awesome-icon>
          泄露信息管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="container" v-loading="loading">
      <el-table :data="leaksTable" style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="data">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="完整代码">
                <a class="url" :href="data.row.url">{{data.row.url}}</a>
              </el-form-item>
              <el-form-item label="原始代码">
                <a class="url" :href="data.row.full_code_url">{{data.row.full_code_url}}</a>
              </el-form-item>
              <el-form-item label="代码段">
                <pre style="line-height: normal">{{data.row.code}}</pre>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="#" prop="id" width="100px"></el-table-column>
        <el-table-column label="泄露信息" prop="name">
          <template slot-scope="scope">
            <span>[{{scope.row.author}}/{{scope.row.repoName}}] {{scope.row.path}}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100px">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 1" type="success" size="small">待确认</el-tag>
            <el-tag v-else-if="scope.row.status === 2" type="danger" size="small">确认泄露</el-tag>
            <el-tag v-else-if="scope.row.status === 3" type="default" size="small">误报</el-tag>
            <el-tag v-else type="default" size="small">未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200px">
          <template slot-scope="scope">
            <el-dropdown trigger="click" @command="handleCommand">
              <el-button type="primary" size="small">
                更多操作 <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="confirm" :disabled="scope.row.status === 2">确认泄露</el-dropdown-item>
                <el-dropdown-item command="ignore" :disabled="scope.row.status === 3">设为误报</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-button size="small" type="danger" style="margin: auto 5px"
                       @click="handleDelete(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>

  import leakService from "@/services/leaks";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "leaks",
    data() {
      return {
        // 表格Array
        leaksTable: [],
        loading: false,
        optButtonText: "操作",
      }
    },
    computed: {},
    mounted() {
      this.loading = true;
      leakService.getLeaks(this, 1, 0)
        .then(resp => {
          let data = resp.data;
          if (data.code === 1001) {
            this.leaksTable = data.data;
          } else {
            this.$message.error(data.message);
          }
        })
        .catch(err => {
          this.$message.error(ApiConstant.error_500);
          console.error("error:", err);
        })
        .then(() => {
          this.loading = false;
        });
    },
    methods: {
      handleDelete(idx, row) {
        leakService.deleteLeak(this, row.id)
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              this.$message.success(data.message);
              this.leaksTable.splice(idx, 1);
            } else {
              this.$message.error(data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.error("error:", err);
          })
      },

      handleCommand(command) {
        if (command === "confirm") {}
      }

    }
  }
</script>

<style>
  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
  }

  .url {
    text-decoration: none;
    color: #606266;
  }

  .url:visited {
    text-decoration: none;
    color: #606266;
  }
</style>
