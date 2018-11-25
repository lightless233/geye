<template>
  <item-card class="box-card" shadow="hover">
    <div slot="header" class="clearfix">
      <span>{{item.title}}</span>
    </div>
    <div slot="content">
      <pre>{{item.code}}</pre>
    </div>
    <div slot="footer">
      <el-row style="padding: 20px">
        <el-col :span="12">
          <el-button-group>
            <el-button size="small" type="success" style="width: 100px">确 认</el-button>
            <el-button size="small" type="primary" style="width: 100px">详 情</el-button>
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
    }
  }
</script>

<style scoped>
</style>
