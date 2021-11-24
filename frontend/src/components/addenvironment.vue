<template>
  <div>
    <el-form  :model="addenvironment">
  <el-form-item label="项目编号">
    <el-input v-model="addenvironment.projectCode" disabled></el-input>
  </el-form-item>
      <el-form-item label="环境名称">
    <el-input  v-model="addenvironment.environmentName"></el-input>
  </el-form-item>
       <el-form-item label="环境描述">
    <el-input  v-model="addenvironment.environmentDescription"></el-input>
  </el-form-item>
       <el-form-item label="ip">
<el-input  v-model="addenvironment.ip"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addEnvironment">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>
<script>
export default {
  data () {
    return {
      addenvironment: {
        projectCode: this.$route.query.projectCode,
        environmentName: '',
        environmentDescription: '',
        ip: ''
      }
    }
  },
  methods: {
    addEnvironment () {
      this.$http.post('Environment/addEnvironment', this.addenvironment).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/projectlist') }
      })
    },
    cancel () {
      this.$router.push('/projectlist')
    }
  }
}
</script>

<style scoped>

</style>
