<template>
  <div>
    <el-form  :model="addtestcaseset">
      <el-form-item label="用例集名称">
        <el-input  v-model="addtestcaseset.testcasesetName"></el-input></el-form-item>
      <el-form-item label="用例集编号">
        <el-input  v-model="addtestcaseset.testcasesetCode"></el-input></el-form-item>
       <el-form-item label="项目编号">
    <el-select v-model="addtestcaseset.projectCode"  placeholder="项目编号" @change="gettestcaselist">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
      <el-form-item><el-transfer v-model="addtestcaseset.testcaselist" :data="testcaselist_options" target-order="push"></el-transfer></el-form-item>
      <el-form-item>

    <el-button type="primary" @click="addTestcaseset">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      testcaselist_options: [],
      addtestcaseset: {
        projectCode: '',
        testcasesetName: '',
        testcasesetCode: '',
        testcaselist: []
      },
      projectlist: this.projectList()

    }
  },
  methods: {

    addTestcaseset () {
     var  addtestcaseset_param ={
        projectCode:this.addtestcaseset.projectCode,
        testcasesetName: this.addtestcaseset.testcasesetName,
        testcasesetCode: this.addtestcaseset.testcasesetCode,
        testcaselist: JSON.stringify(this.addtestcaseset.testcaselist)
      }
      this.$http.post('TestCaseSet/AddTestCaseSet', addtestcaseset_param).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/testcasesetlist') }
      })
    },
    cancel () {
      this.$router.push('/testcasesetlist')
    },
    projectList () {
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
        }
      })
    },
    gettestcaselist(){
      this.testcaselist_options=[]
      this.addtestcaseset.testcaselist=[]
          this.$http.post('TestCase/testcaselist', {projectCode: this.addtestcaseset.projectCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          if (response.data.data.length!==0) {
            for (var i = 0, len = response.data.data.length; i < len; i++) {
              this.testcaselist_options.push({
                key: response.data.data[i].testcaseCode,
                label: response.data.data[i].testcaseName
              })
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
