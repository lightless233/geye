<template>
  <div>
    <item-card class="box-card" shadow="hover" v-show="hasShow">
      <div slot="header" class="clearfix title">
        <div style="margin-bottom: 10px">
          <span @click="handleClickTitle" class="url">[{{item.author}}/{{item.repoName}}] {{item.path}}</span>
        </div>
        <el-tag size="mini" type="info" class="tag">ID: {{item.id}}</el-tag>
        <el-tag size="mini" type="info" class="tag">{{item.searchRuleName}} - {{item.filterRuleName}}</el-tag>
        <el-tag size="mini" type="info" class="tag">发现时间: {{item.created_time}}</el-tag>
        <el-tag size="mini" type="info" class="tag">{{item.sha}}</el-tag>
      </div>
      <div slot="content">
        <pre style="overflow-y: auto">{{item.code}}</pre>
      </div>
      <div slot="footer">
        <el-row style="padding: 20px">
          <el-col :span="12">
            <el-button-group>
              <el-button size="small" type="success" style="width: 100px" @click="handleConfirm">确 认</el-button>
              <el-button size="small" type="primary" style="width: 100px" @click="handleRawCode">详 情</el-button>
              <el-button size="small" type="danger" style="width: 100px" @click="handleIgnore">忽 略</el-button>
            </el-button-group>
          </el-col>
          <el-col :span="12" style="text-align: right">
            <el-dropdown trigger="click">
              <el-button size="small" type="default">更多操作<i class="el-icon-arrow-down el-icon--right"></i></el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="isShowConvertDialog = true">规则转化</el-dropdown-item>
                <el-dropdown-item>clone并上传到OSS保存</el-dropdown-item>
                <el-dropdown-item>推送到其他系统</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
        </el-row>
      </div>

    </item-card>
    <rule-converter :isOpen.sync="isShowConvertDialog" :item="item"></rule-converter>
  </div>
</template>

<script>

  import itemCard from "@/components/utils/ItemCard";
  import searchResultsService from "@/services/handleCenter/searchCenter";
  import ApiConstant from "@/utils/constant";
  import RuleConverter from "@/components/handleCenter/utils/ruleConverter";

  export default {
    name: "searchResultItem",
    // 需要从父组件接受的值放在props里面
    props: ["item"],
    components: {
      "rule-converter": RuleConverter,
      ItemCard: itemCard
    },
    data() {
      return {
        hasShow: true,
        isShowConvertDialog: false,
      }
    },
    methods: {
      handleRawCode: function () {
        window.open(this.item.full_code_url);
      },

      handleIgnore: function () {
        // console.log(this.item);
        searchResultsService.ignore(this, {"id": this.item.id})
          .then(resp => {
            if (resp.data.code === 1001) {
              this.hasShow = false;
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.log("error:", err);
          });
      },

      handleConfirm: function () {
        searchResultsService.confirm(this, {"id": this.item.id})
          .then(resp => {
            if (resp.data.code === 1001) {
              // this.hasShow = false;
              this.$message.success("已确认信息泄露！")
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.log("error:", err);
          });
      },

      handleClickTitle: function () {
        window.open(this.item.url)
      }
    }
  }
</script>

<style scoped>
  .box-card {
    margin: 20px auto;
  }

  .title {
    font-size: 1.5em;
  }

  .tag {
    margin-right: 5px;
  }

  .url {
    cursor: pointer;
  }
</style>
