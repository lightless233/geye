<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <font-awesome-icon icon="bars" fixed-width></font-awesome-icon>
          Token管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="container">
      <el-table :data="tokenData" style="width: 100%">
        <el-table-column prop="id" label="#" width="100px"></el-table-column>
        <el-table-column prop="token" label="Token"></el-table-column>
        <el-table-column prop="status" label="状态"></el-table-column>
        <el-table-column prop="available" label="可用性"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="primary">编辑</el-button>
            <el-button size="mini" type="danger">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
  export default {
    name: "token",
    data() {
      return {
        tokenData: [{
          "id": 1,
          "token": "12344321123443211234432112344321",
          "status": 1,
          "available": "剩余次数: 20",
        }]
      }
    },
    mounted() {

    },
    methods: {
      handleDelete: function () {

      },
      handleEdit: function () {

      }
    }
  }
</script>

<style scoped>

</style>
