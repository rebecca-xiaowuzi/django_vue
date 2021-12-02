<template>
 <el-button type="primary" @click="add">新增</el-button>
</template>

<script>
export default {
  methods: {
    add () {
      this.$router.push({path: '/childapi', query: {projectCode: 'jilianyun'}})
    }}
}
</script>

<style scoped>

</style>
