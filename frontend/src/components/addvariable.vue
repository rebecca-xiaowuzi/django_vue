<template>
  <div>
    <el-form  :model="addvariable">
  <el-form-item label="项目编号">
   <el-select v-model="addvariable.projectCode"  placeholder="项目编号" @change="getprojectlist">
       <el-option
      v-for="(item,index) in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="index">
    </el-option>
    </el-select>
  </el-form-item>
      <el-form-item label="环境名称">
    <el-select v-model="addvariable.environmentName" placeholder="环境名称">
       <el-option
      v-for="item in environments"
      :key="item.environmentName"
      :label="item.environmentName"
      :value="item.environmentName">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="变量名称">
    <el-input  v-model="addvariable.variableName"></el-input>
  </el-form-item>
       <el-form-item label="变量值">
   <el-input  v-model="addvariable.variable"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addVariable">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      addvariable: {
        projectCode: '',
        environmentName: '',
        variableName: '',
        variable: ''
      },
      projectlist: this.getprojectlist(),
      environments: '',
      index: 0
    }
  },
  methods: {
    addVariable () {
      this.$http.post('Environment/addVariable', this.addvariable).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/variablelist') }
      })
    },
    cancel () {
      this.$router.push('/variablelist')
    },
    getprojectlist (val) {
      this.index = val
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
          // 项目下拉框设置默认值
          this.addvariable.projectCode = response.data.data[this.index].projectCode
          // 判断项目下是否有环境变量 有 获取列表 给默认值
          if (response.data.data[this.index].environments.length !== 0) {
            this.environments = response.data.data[this.index].environments
            this.addvariable.environmentName = response.data.data[this.index].environments[0].environmentName
          } else { this.addvariable.environmentName = ''; this.environments = [] }// 无环境信息时，清空输入框数据
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
