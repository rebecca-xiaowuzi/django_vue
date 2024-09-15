<template>
  <div>
    <el-form  :model="updatesql">
       <el-form-item label="sql名称">
    <el-input  v-model="updatesql.sqlName" disabled></el-input>
  </el-form-item>
       <el-form-item label="sql编号">
   <el-input  v-model="updatesql.sqlCode" disabled></el-input>
  </el-form-item>
      <el-form-item label="sql">
   <el-input  v-model="updatesql.sql"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateSql">修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      updatesql: {
        sqlName: this.getSqlDetail(),
        sqlCode: '',
        sql: ''
      }

    }
  },
  methods: {
    updateSql () {
      this.$http.post('Sql/UpdateSql', this.updatesql).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/sqllist') }
      })
    },
    cancel () {
      this.$router.push('/sqllist')
    },
    getSqlDetail () {
      this.$http.post('Sql/getsqlDetail', {sqlCode:this.$route.query.sqlCode}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.updatesql = response.data.data }
      })
    },
  }
}
</script>

<style scoped>

</style>
