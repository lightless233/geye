<template>
  <div class="main-div" v-loading="loading">
    <search-result-item :item=item></search-result-item>
  </div>
</template>
<script>

  import searchResultItem from "@/components/utils/searchResultItem"
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
        items: {
          title: "aaa",
          code: "aaaa\nbbbb\nccc"
        }
      }
    },
  }
</script>

<style scoped>

</style>
