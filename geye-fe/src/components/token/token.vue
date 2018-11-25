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
      <div>
        <el-button type="primary" size="small" round @click="handleOpenDialog('add', -1, null)">添加Token</el-button>
      </div>
      <el-table :data="tokenData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="#" width="100px"></el-table-column>
        <el-table-column prop="tokenName" label="Token名称"></el-table-column>
        <el-table-column prop="tokenContent" label="Token"></el-table-column>
        <el-table-column prop="status" label="状态"></el-table-column>
        <el-table-column prop="remainLimit" label="可用次数"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleOpenDialog('edit', scope.$index, scope.row)">编辑
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>


    <!-- 添加token的dialog -->
    <el-dialog :title="dialogTitle" :visible.sync="showTokenDialog">
      <el-form label-width="100px" :model="tokenForm" :disabled="isDisableForm">
        <el-form-item label="Token名称">
          <el-input v-model="tokenForm.tokenName" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Token">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}" v-model="tokenForm.tokenContent"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="tokenForm.status" :value="1" style="max-width: 100%">
            <el-option label="关闭" :value="0"></el-option>
            <el-option label="开启" :value="1"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleConfirm">{{dialogConfirmButtonText}}</el-button>
        <el-button type="danger" @click="showTokenDialog = false">关闭</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

  import tokenService from "@/services/token";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "token",
    data() {
      return {
        tokenData: [],
        loading: false,

        // 表单数据
        tokenForm: {
          tokenName: "",
          tokenContent: "",
          status: 1,
        },

        // dialog 相关的变量
        showTokenDialog: false,
        dialogTitle: "添加新Token",
        isDisableForm: false,
        dialogConfirmButtonText: "",
        dialogType: "",
      }
    },
    mounted() {
      this.loading = true;
      tokenService.getAllTokens(this)
        .then(resp => {
          if (resp.data.code === 1001) {
            this.tokenData = resp.data.data;
          } else {
            this.$message.error(resp.data.message);
          }
        })
        .catch(err => {
          console.log("error: ", err);
          this.$message.error(ApiConstant.error_500);
        })
        .then(() => {
          this.loading = false;
        })
    },
    methods: {

      initForm: function () {
        this.tokenForm.tokenName = "";
        this.tokenForm.tokenContent = "";
        this.tokenForm.status = 1;
      },

      handleDelete: function (tableIdx, row) {
        let tokenId = row.id;
        tokenService.deleteToken(this, {"id": tokenId})
          .then(resp => {
            if (resp.data.code === 1001) {
              this.tokenData.splice(tableIdx, 1);
              this.$message.success(resp.data.message);
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            console.log("error: ", err);
            this.$message.error(ApiConstant.error_500);
          });
      },

      handleEdit: function () {

      },

      handleAddToken: function () {

      },

      handleConfirm: function () {
        if (this.dialogType === "add") {
          tokenService.addToken(this, this.tokenForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                this.tokenData.push(resp.data.data);
                this.showTokenDialog = false;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(err => {
              console.log("error: ", err);
              this.$message.error(ApiConstant.error_500);
            });
        } else if (this.dialogType === "edit") {

        } else {
          this.$message.error("未知错误");
        }
      },

      handleOpenDialog: function (type, tableIdx, row) {
        if (type === "add") {
          this.dialogTitle = "添加Token";
          this.dialogConfirmButtonText = "添加";
          this.dialogType = type;
          this.initForm();
          this.showTokenDialog = true;
        } else if (type === "edit") {

        } else {
          this.$message.error("未知错误");
        }
      },
    }
  }
</script>

<style scoped>

</style>
