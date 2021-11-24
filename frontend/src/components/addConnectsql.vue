<template>
  <div>
    <el-form  :model="addConnectsql">
  <el-form-item label="项目编号">
   <el-select v-model="addConnectsql.projectCode"  placeholder="项目编号" @change="getprojectlist">
       <el-option
      v-for="(item,index) in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="index">
    </el-option>
    </el-select>
  </el-form-item>
      <el-form-item label="环境名称">
    <el-select v-model="addConnectsql.environmentName" placeholder="环境名称">
       <el-option
      v-for="item in environments"
      :key="item.environmentName"
      :label="item.environmentName"
      :value="item.environmentName">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="连接名称">
    <el-input  v-model="addConnectsql.sqlconnectName"></el-input>
  </el-form-item>
       <el-form-item label="连接编号">
   <el-input  v-model="addConnectsql.sqlconnectCode"></el-input>
  </el-form-item>
      <el-form-item label="host">
   <el-input  v-model="addConnectsql.host"></el-input>
  </el-form-item>
      <el-form-item label="端口">
   <el-input  v-model="addConnectsql.port"></el-input>
  </el-form-item>
      <el-form-item label="用户名">
   <el-input  v-model="addConnectsql.username"></el-input>
  </el-form-item>
      <el-form-item label="密码">
   <el-input  v-model="addConnectsql.password"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addConnectSql">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      addConnectsql: {
        projectCode: '',
        environmentName: '',
        sqlconnectName: '',
        sqlconnectCode: '',
        host: '',
        port: '',
        username: '',
        password: ''
      },
      projectlist: this.getprojectlist(),
      environments: '',
      index: 0
    }
  },
  methods: {
    addConnectSql () {
      this.$http.post('Sql/AddSqlConnect', this.addConnectsql).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/SqlConnectlist') }
      })
    },
    cancel () {
      this.$router.push('/SqlConnectlist')
    },
    getprojectlist (val) {
      this.index = val
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
          // 项目下拉框设置默认值
          this.addConnectsql.projectCode = response.data.data[this.index].projectCode
          // 判断项目下是否有环境变量 有 获取列表 给默认值
          if (response.data.data[this.index].environments.length !== 0) {
            this.environments = response.data.data[this.index].environments
            this.addConnectsql.environmentName = response.data.data[this.index].environments[0].environmentName
          } else { this.addConnectsql.environmentName = ''; this.environments = [] }// 无环境信息时，清空输入框数据
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
