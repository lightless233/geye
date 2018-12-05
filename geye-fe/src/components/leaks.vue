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

      <el-row>
        <el-dropdown trigger="click" @command="handleSelectionCommand">
          <el-button type="primary" size="small">
            选中项 <i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item :command="{'action': 'confirm'}">确认泄露</el-dropdown-item>
            <el-dropdown-item :command="{'action': 'ignore'}">设为误报</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-row>

      <el-table :data="leaksTable" ref="refTable" style="width: 100%" v-on:filter-change="filterChange"
                @selection-change="handleSelectionChange" @row-click="handleRowClick" row-key="id">
        <!-- 复选框 -->
        <el-table-column type="selection" width="55"></el-table-column>

        <!-- 折叠起来的内容 -->
        <el-table-column type="expand">
          <template slot-scope="data">
            <el-form label-position="left" class="demo-table-expand">
              <el-form-item label="完整代码">
                <a class="url" :href="data.row.url">点我查看</a>
              </el-form-item>
              <el-form-item label="原始代码">
                <a class="url" :href="data.row.full_code_url">点我查看</a>
              </el-form-item>
              <el-form-item label="命中规则">
                <span>{{data.row.searchRuleName}} || {{data.row.filterRuleName}}</span>
              </el-form-item>
              <el-form-item label="代码段">
                <pre style="line-height: normal; padding-left: 90px; overflow-y: auto">{{data.row.code}}</pre>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="#" prop="id" width="100px"></el-table-column>
        <!--<el-table-column label="泄露信息" prop="name">-->
        <!--<template slot-scope="scope">-->
        <!--<span>[{{scope.row.author}}/{{scope.row.repoName}}] {{scope.row.path}}</span>-->
        <!--</template>-->
        <!--</el-table-column>-->
        <el-table-column label="作者" prop="author"></el-table-column>
        <el-table-column label="仓库名称" prop="repoName"></el-table-column>
        <el-table-column label="文件名" prop="path" width="400px"></el-table-column>

        <el-table-column label="状态" width="100px" prop="status" column-key="status" :filters="statusFilterMenu">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 1" type="success" size="small">待确认</el-tag>
            <el-tag v-else-if="scope.row.status === 2" type="danger" size="small">确认泄露</el-tag>
            <el-tag v-else-if="scope.row.status === 3" type="default" size="small">误报</el-tag>
            <el-tag v-else type="default" size="small">未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发现时间" prop="created_time" width="100px"></el-table-column>
        <el-table-column label="操作" width="200px">
          <template slot-scope="scope">
            <el-dropdown trigger="click" @command="handleCommand">
              <el-button type="primary" size="small">
                更多操作 <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                    :command="{'action': 'confirm', 'row': scope.row, 'idx': scope.$index}"
                    :disabled="scope.row.status === 2">确认泄露
                </el-dropdown-item>
                <el-dropdown-item :command="{'action': 'ignore', 'row': scope.row, 'idx': scope.$index}"
                                  :disabled="scope.row.status === 3">设为误报
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-button size="small" type="danger" style="margin: auto 5px"
                       @click="handleDelete(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <div class="block" style="margin-top: 20px" align="center">
        <el-pagination
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-size="20"
            layout="total, prev, pager, next"
            :total="totalCount">
        </el-pagination>
      </div>
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

        // constant
        ALL_STATUS_LEAK: "1,2,3",

        // 表格Array
        leaksTable: [],
        loading: false,
        optButtonText: "操作",

        // status 过滤菜单
        statusFilterMenu: [
          {text: '待处理', value: 1},
          {text: '确认泄露', value: 2},
          {text: '误报', value: 3},
        ],

        // 分页相关
        currentPage: 1,
        totalCount: 0,

        // 复选框相关
        multiSelectionItems: [],
      }
    },
    computed: {},
    mounted() {
      this.loading = true;
      leakService.getLeaks(this, 1, this.ALL_STATUS_LEAK)
        .then(resp => {
          let data = resp.data;
          if (data.code === 1001) {
            this.leaksTable = data.data;
            this.totalCount = data.total_count;
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
              // 总量记得减1
              this.totalCount -= 1;
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
        /*
        处理下拉菜单的操作
         */
        console.log("command:", command);
        let action = command.action;
        let row = command.row;
        let idx = command.idx;
        let id = row.id;

        if (action !== "confirm" && action !== "ignore") {
          this.$message.error("未知操作!");
          return;
        }

        leakService.changeStatusLeak(this, action, id)
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              let newValue = 0;
              if (action === "ignore") {
                newValue = 3;
              } else if (action === "confirm") {
                newValue = 2;
              } else {
                this.$message.error("Error Action!");
                return;
              }
              row.status = newValue;
              this.leaksTable.splice(idx, 1, row);
              this.$message.success(data.message);
            } else {
              this.$message.error(data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.error("error:", err);
          });
      },

      /*
      处理复选框的下拉菜单
       */
      handleSelectionCommand(command) {
        // console.log(command);
        // console.log(this.multiSelectionItems);

        console.log(this.leaksTable.filter(t => this.multiSelectionItems.some(s => s.id === t.id)));

        let action = command.action;
        let ids = [];
        for (const item of this.multiSelectionItems) {
          ids.push(item.id);
        }

        if (action !== "confirm" && action !== "ignore") {
          this.$message.error("unknown action!");
          return;
        }
        if (ids.length === 0) {
          this.$message.error("请先选择要处理的数据!");
          return;
        }

        let newStatus = 1;
        if (action === "confirm") {
          newStatus = 2;
        } else if (action === "ignore") {
          newStatus = 3;
        }

        this.loading = true;
        // request API for batch update status
        leakService.batchChangeStatusLeak(this, action, ids)
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              this.$message.success(data.message);
              // See: https://segmentfault.com/q/1010000007849369
              let updatedRows = this.leaksTable.filter(t => this.multiSelectionItems.some(s => s.id === t.id));
              for (const row of updatedRows) {
                row.status = newStatus;
              }
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
          })

      },

      handleRowClick(row, event, column) {
        this.$refs.refTable.toggleRowSelection(row)
      },

      handleCurrentChange(val) {
        // val就是改变后的页码，有了.sync修饰，应该不需要手工变更页码
        this.currentPage = val;
        this.loading = true;
        leakService.getLeaks(this, val, this.ALL_STATUS_LEAK)
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              this.leaksTable = data.data;
              this.totalCount = data.total_count;
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

      // filterStatus(value, row, column) {
      //   // console.log("value:", value, " || row:", row);
      //   return row.status === value;
      // },

      filterChange(filter) {
        console.log("filter:", filter);
        this.loading = true;

        let filterStatus = filter.status;
        let queryStatus = "";

        if (filterStatus.length === 0) {
          queryStatus = this.ALL_STATUS_LEAK;
        } else {
          queryStatus = filterStatus.join(",");
        }

        leakService.getLeaks(this, 1, queryStatus)
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              this.currentPage = 1;
              this.totalCount = data.total_count;
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
          })
      },

      handleSelectionChange(val) {
        // 处理多选框的情况
        // val就是选中的行，是个array
        console.log(val);
        this.multiSelectionItems = val;
      },
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

  .url {
    text-decoration: none;
    color: #606266;
  }

  .url:visited {
    text-decoration: none;
    color: #606266;
  }
</style>
