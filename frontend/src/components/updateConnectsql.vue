<template>
  <div>
    <el-form  :model="updateConnectsql">
  <el-form-item label="项目编号">
   <el-input v-model="updateConnectsql.projectCode"  placeholder="项目编号" disabled>
    </el-input>
  </el-form-item>
      <el-form-item label="环境名称">
    <el-input v-model="updateConnectsql.environmentName" placeholder="环境名称" disabled>
    </el-input>
  </el-form-item>
       <el-form-item label="连接名称">
    <el-input  v-model="updateConnectsql.sqlconnectName" disabled></el-input>
  </el-form-item>
       <el-form-item label="连接编号">
   <el-input  v-model="updateConnectsql.sqlconnectCode" disabled></el-input>
  </el-form-item>
      <el-form-item label="host">
   <el-input  v-model="updateConnectsql.host"></el-input>
  </el-form-item>
      <el-form-item label="端口">
   <el-input  v-model="updateConnectsql.port"></el-input>
  </el-form-item>
      <el-form-item label="用户名">
   <el-input  v-model="updateConnectsql.username"></el-input>
  </el-form-item>
      <el-form-item label="密码">
   <el-input  v-model="updateConnectsql.password"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateConnectSql">修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      updateConnectsql: {
        projectCode: this.getConnectSqlDetail(),
        environmentName: '',
        sqlconnectName: '',
        sqlconnectCode: '',
        host: '',
        port: '',
        username: '',
        password: ''
      }
    }
  },
  methods: {
    getConnectSqlDetail () {
      this.$http.post('Sql/getsqlconnectDetail', {projectCode: this.$route.query.projectCode, environmentName: this.$route.query.environmentName, sqlconnectCode: this.$route.query.sqlconnectCode}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.updateConnectsql = response.data.data }
      })
    },
    updateConnectSql () {
      this.$http.post('Sql/UpdateSqlConnect', this.updateConnectsql).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/SqlConnectlist') }
      })
    },
    cancel () {
      this.$router.push('/SqlConnectlist')
    }
  }
}
</script>

<style scoped>

</style>
