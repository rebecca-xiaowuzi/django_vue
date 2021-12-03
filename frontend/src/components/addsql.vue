<template>
  <div>
    <el-form  :model="addsql">
       <el-form-item label="sql名称">
    <el-input  v-model="addsql.sqlName"></el-input>
  </el-form-item>
       <el-form-item label="sql编号">
   <el-input  v-model="addsql.sqlCode"></el-input>
  </el-form-item>
      <el-form-item label="sql">
   <el-input  v-model="addsql.sql"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addSql">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      addsql: {
        sqlName: '',
        sqlCode: '',
        sql: ''
      }
    }
  },
  methods: {
    addSql () {
      this.$http.post('Sql/AddSql', this.addsql).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/sqllist') }
      })
    },
    cancel () {
      this.$router.push('/sqllist')
    }
  }
}
</script>

<style scoped>

</style>
