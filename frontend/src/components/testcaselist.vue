<template>
  <el-form><el-form-item><el-button type="primary" @click="add">新增用例</el-button></el-form-item><el-form-item><el-button type="primary" @click="add2">新增sql</el-button></el-form-item></el-form>

</template>

<script>
export default {
  methods: {
    add () {
      this.$router.push({path: '/addtestcase'})
    },
    add2 () {
      this.$router.push({path: '/childsql', query: {projectCode: 'jilianyun'}})
    }
  }
}
</script>

<style scoped>

</style>
