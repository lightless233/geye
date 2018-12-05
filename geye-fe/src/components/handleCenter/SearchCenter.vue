<template>
  <div class="main-div" v-loading="loading">
    <div v-if="items.length">
      <search-result-item v-for="item in items" :item="item"></search-result-item>
      <div align="center">
        <el-button type="primary" style="width: 100%" align="center" @click="handleLoadMore">加载更多</el-button>
      </div>
    </div>
    <div v-else>
      <el-tag style="width: 100%" align="center">暂无数据</el-tag>
    </div>
  </div>
</template>
<script>

  import searchResultItem from "@/components/handleCenter/utils/searchResultItem"
  import resultsService from "@/services/handleCenter/searchCenter"
  import ApiConstant from "@/utils/constant"

  export default {
    name: "SearchCenter",
    components: {
      "search-result-item": searchResultItem
    },
    mounted() {
      this.loading = true;
      resultsService.getAllSearchResults(this, {page: 1})
        .then(resp => {
          if (resp.data.code === 1001) {
            this.items = resp.data.data;
          } else {
            this.$message.error(resp.data.message);
          }
        })
        .catch(err => {
          console.error("error:", err);
          this.$message.error(ApiConstant.error_500);
        })
        .then(() => {
          this.loading = false;
        })
    },
    data() {
      return {
        loading: false,
        items: [],
        currentPage: 1,
      }
    },
    methods: {
      handleLoadMore: function () {
        this.currentPage += 1;
        resultsService.getAllSearchResults(this, {page: this.currentPage})
          .then(resp => {
            let data = resp.data;
            if (data.code === 1001) {
              if (data.data.length) {
                for (const datum of data.data) {
                  this.items.push(datum);
                }
              } else {
                this.$message.error("没有更多内容啦!");
              }
            } else {
              this.$message.error(data.message);
            }
          })
          .catch(err => {
            this.$message.error(ApiConstant.error_500);
            console.error("error:", err);
          })
      }
    }
  }
</script>

<style scoped>

</style>
