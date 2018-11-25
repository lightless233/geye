<template>
  <search-result-item :item=item></search-result-item>
</template>

<script>

  import searchResultItem from "@/components/utils/searchResultItem"

  export default {
    name: "SearchCenter",
    components: {
      "search-result-item": searchResultItem
    },
    data() {
      return {
        item: {
          title: "aaa",
          code: "aaaa\nbbbb\nccc"
        }
      }
    },
  }
</script>

<style scoped>

</style>
