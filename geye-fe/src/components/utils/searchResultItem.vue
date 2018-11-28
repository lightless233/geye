<template>
  <item-card class="box-card" shadow="hover">
    <div slot="header" class="clearfix title">
      <div style="margin-bottom: 10px">
        <span>[{{item.author}}/{{item.repoName}}] {{item.path}}</span>
      </div>
      <el-tag size="mini" type="info" class="tag">{{item.searchRuleName}} - {{item.filterRuleName}}</el-tag>
      <el-tag size="mini" type="info" class="tag">发现时间: {{item.created_time}}</el-tag>
      <el-tag size="mini" type="info" class="tag">{{item.sha}}</el-tag>
    </div>
    <div slot="content">
      <pre>{{item.code}}</pre>
    </div>
    <div slot="footer">
      <el-row style="padding: 20px">
        <el-col :span="12">
          <el-button-group>
            <el-button size="small" type="success" style="width: 100px">确 认</el-button>
            <el-button size="small" type="primary" style="width: 100px" @click="handleRawCode">详 情</el-button>
            <el-button size="small" type="danger" style="width: 100px">忽 略</el-button>
          </el-button-group>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-dropdown trigger="click">
            <el-button size="small" type="default">更多操作<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>推送到其他系统</el-dropdown-item>
              <el-dropdown-item>clone并上传到OSS保存</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-col>
      </el-row>
    </div>
  </item-card>
</template>

<script>

  import itemCard from "@/components/utils/ItemCard";

  export default {
    name: "searchResultItem",
    // 需要从父组件接受的值放在props里面
    props: ["item"],
    components: {
      "ItemCard": itemCard
    },
    methods: {
      handleRawCode: function () {
        window.open(this.item.full_code_url);
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
</style>
