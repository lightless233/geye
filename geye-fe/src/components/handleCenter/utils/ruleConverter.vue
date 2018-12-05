<template>
  <!-- 规则转化的组件 -->
  <el-dialog title="快速规则转化" :visible.sync="isOpen" center :before-close="onClose" v-loading="loading" width="75%">
    <el-steps :active="active" finish-status="success" style="margin-bottom: 40px">
      <el-step title="选择转化内容"></el-step>
      <el-step title="完善规则"></el-step>
      <el-step title="完成"></el-step>
    </el-steps>

    <el-row v-if="active === 0">
      <el-form label-width="100px">
        <el-form-item label="规则类型">
          <el-select v-model="convertType" value="" style="width: 100%">
            <el-option label="全局规则" value="0"></el-option>
            <el-option :label="'当前搜索规则(' + item.searchRuleName + ')'" :value="item.srid"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="转换内容">
          <el-select v-model="convertContent" value="" style="width: 100%">
            <el-option :label="'仓库作者: ' + item.author" :value="{position: 1, value: item.author}"></el-option>
            <el-option :label="'仓库名称: ' + item.repoName" :value="{position: 2, value: item.repoName}"></el-option>
            <el-option :label="'文件路径: ' + item.path" :value="{position: 3, value: item.path}"></el-option>
            <el-option :label="'代码内容: '" :value="{position: 4, value: '请输入规则内容...'}"></el-option>
            <el-option :label="'文件名: ' + item.filename" :value="{position: 5, value: item.filename}"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row v-else-if="active === 1">
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="规则标题">
          <el-input v-model="ruleForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="规则内容">
          <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}" v-model="ruleForm.ruleContent"/>
        </el-form-item>

        <el-row>
          <el-col :span="8">
            <el-form-item label="规则引擎">
              <el-select v-model="ruleForm.ruleEngine" :value="2" style="width: 100%;">
                <el-option label="正则引擎" :value="1"></el-option>
                <el-option label="串匹配引擎" :value="2"></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="优先级">
              <el-input v-model="ruleForm.priority" autocomplete="off" type="number"/>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="ruleForm.status" :value="1" style="width: 100%;">
                <el-option label="开启" :value="1"></el-option>
                <el-option label="关闭" :value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="8">
            <!--rule type-->
            <el-form-item label="规则类型">
              <el-select v-model="ruleForm.ruleType" :value="1" style="width: 100%;">
                <el-option label="正向匹配" :value="1"/>
                <el-option label="反向匹配" :value="2"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <!--position-->
            <el-form-item label="匹配位置">
              <el-select v-model="ruleForm.position" :value="4" style="width: 100%;">
                <el-option label="仓库作者" :value="1"/>
                <el-option label="仓库名称" :value="2"/>
                <el-option label="文件路径" :value="3"/>
                <el-option label="代码内容" :value="4"/>
                <el-option label="文件名" :value="5"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <!--action-->
            <el-form-item label="命中操作">
              <el-select v-model="ruleForm.action" :value="5" style="width: 100%;">
                <el-option label="继续匹配下一条规则" :value="1"/>
                <el-option label="设为误报-不保存" :value="2"/>
                <el-option label="设为误报-保存" :value="3"/>
                <el-option label="设为确认-保存" :value="4"/>
                <el-option label="设为待确认-保存" :value="5"/>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-row>
    <el-row v-else>
      Error!
    </el-row>

    <span slot="footer" class="dialog-footer">
      <el-button @click="onClose">取消</el-button>
      <el-button type="primary" @click="handlePrevious" :disabled="this.active === 0">上一步</el-button>
      <el-button type="primary" @click="handleNext">下一步</el-button>
    </span>
  </el-dialog>
</template>

<script>

  import globalFilterService from "@/services/globalFilterRule";
  import filterService from "@/services/filterRule";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "ruleConverter",
    // 从父组件接受的对象item，包含一条leaks信息
    props: ["item", "isOpen"],
    data() {
      return {
        active: 0,
        loading: false,

        // 第一步的数据
        convertType: "",
        convertContent: "",

        // 第二步的数据
        ruleForm: {
          id: 0,
          name: "",
          ruleContent: "",
          ruleEngine: 2,
          priority: 5,
          status: 1,
          ruleType: 1,
          position: 4,
          action: 5
        }
      }
    },
    mounted() {
      //alert("rule conveter mounted!")
    },
    methods: {
      /*
      关闭时执行，需要通知父组件关闭事件
       */
      onClose: function () {
        this.$emit("update:isOpen", false);
      },

      /*
      初始化相关数据
      */
      clearData: function () {
        this.active = 0;
        this.convertType = "";
        this.convertContent = "";
        this.ruleForm = {
          id: 0,
          name: "",
          ruleContent: "",
          ruleEngine: 2,
          priority: 5,
          status: 1,
          ruleType: 1,
          position: 4,
          action: 5
        }
      },

      /*
      点击上一步按钮
       */
      handlePrevious: function () {
        this.active = this.active - 1 >= 0 ? this.active - 1 : 0;
      },

      // 点击下一步按钮
      handleNext: function () {
        if (this.active === 0) {
          // 先校验数据是否都有，然后再增加active
          if (!this.convertType) {
            this.$message.error("请先选择规则类型!");
            return;
          }

          if (!this.convertContent) {
            this.$message.error("请选择转化内容!");
            return;
          }

          // 填充数据，准备进入下一步
          this.ruleForm.position = this.convertContent.position;
          this.ruleForm.ruleContent = this.convertContent.value;
          this.ruleForm.id = this.convertType;
          this.ruleForm.name = "快速转换规则-" + new Date().getTime();
          this.active++;
        } else if (this.active === 1) {
          // console.log("convertContent:", this.convertContent);
          // console.log("form: ", this.ruleForm);

          this.loading = true;

          // 提交数据到后端
          let promise = null;
          if (Number.parseInt(this.ruleForm.id) === 0) {
            promise = globalFilterService.addGlobalFilterRule(this, this.ruleForm)
          } else {
            promise = filterService.addFilterRule(this, this.ruleForm)
          }

          promise
            .then(resp => {
              let data = resp.data;
              if (data.code === 1001) {
                this.$message.success("规则转换成功, 可至相关规则页查看详情!");
                this.onClose();
                // 清空active和数据
                this.clearData()
              } else {
                this.$message.error(data.message);
              }
            })
            .catch(err => {
              console.error("error:", err);
              this.$message.error(ApiConstant.error_500);
            })
            .then(() => {
              this.loading = false;
            })
        } else {
          this.$message.error("Unknown active!");
        }
      }
    }
  }
</script>

<style scoped>

</style>
