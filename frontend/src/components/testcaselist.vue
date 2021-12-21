<template>
  <div>
  <el-form :inline="true" :model="searchtestcase" class="demo-form-inline">
    <el-form-item label="项目编号">
    <el-select v-model="searchtestcase.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
     <el-form-item label="用例名称">
    <el-input v-model="searchtestcase.testcaseName" placeholder="用例名称"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchTestcase">查询</el-button>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="addTestcase">新增用例</el-button>
  </el-form-item>
</el-form>
  <div>
  <el-table
    :data="tableData"
    border>
    <el-table-column
      fixed
      prop="projectCode"
      label="项目编号">
    </el-table-column>
    <el-table-column
      prop="testcaseName"
      label="用例名称">
    </el-table-column>
    <el-table-column
      prop="testcaseCode"
      label="用例Code">
    </el-table-column>
    <el-table-column
      prop="testcaseModel"
      label="用例所属模块">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button type="text" size="small"  @click="updatetestcase(scope.row)">编辑</el-button>
       <el-dropdown trigger="click" @command="runtestcase">
   <el-button type="primary"  @click ="getenvironmentList(scope.row)">运行</el-button>
  <el-dropdown-menu slot="dropdown">
    <el-dropdown-item v-for="enitem in environmentlist" :command="beforeHandleCommand(scope.row,enitem.environmentName)" v-text="enitem.environmentName"></el-dropdown-item>
  </el-dropdown-menu>
</el-dropdown>
         <el-button type="text" size="small"  @click="copyTestcase(scope.row)">复制</el-button>
      </template>
    </el-table-column>
  </el-table>
  <div class="block">
    <span class="demonstration">显示总数</span>
    <el-pagination
      @current-change="handleCurrentChange"
      :page-size="10"
      layout="total, prev, pager, next"
      :total="total">
    </el-pagination>
  </div>
  </div>
  </div>
</template>
<script>
export default {
  data () {
    return {
      searchtestcase: {
        projectCode: '',
        testcaseName: ''
      },
      projectlist: this.projectList(),
      tableData: [],
      page: 1,
      pagesize: 10,
      total: 0,
      environmentlist:[]
    }
  },
created(){
      this.searchTestcase()
    },
  methods: {
    copyTestcase(row){
       this.$http.post('TestCase/CopyTestcase',{projectCode:row.projectCode, testcaseCode:row.testcaseCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目环境下拉列表数据
         this.searchTestcase()
        }
      })
    },
     getenvironmentList (row) {
      var projectcode = row.projectCode
      this.$http.get(`Environment/getEnvironmentbyprojectcode?projectCode=${projectcode}`).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目环境下拉列表数据
          this.environmentlist = response.data.data
        }
      })
    },
    beforeHandleCommand(row,command){
      return {row,command}
    },
    runtestcase(command){
      this.$http.post('TestCase/runTestCase', {projectCode:command.row.projectCode, testcaseCode:command.row.testcaseCode, environmentName: command.command}).then(response => {
          return this.$message({message: response.data.msg, center: true})
      })

    },
    updatetestcase (row) {
      this.$router.push({path: '/updatetestcase', query: { projectCode: row.projectCode, testcaseCode: row.testcaseCode }})
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
    searchTestcase () {
      this.$http.post('TestCase/testcaselist', {projectCode: this.searchtestcase.projectCode, testcaseName: this.searchtestcase.testcaseName, page: this.page, pagesize: this.pagesize}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.tableData = response.data.data
          this.total = response.data.total
        }
      })
    },
    // 获取页数直接请求list接口
    handleCurrentChange (val) {
      this.page = val
      this.searchTestcase()
    },
    addTestcase () {
      this.$router.push('/addtestcase')
    }
  }
}
</script>

<style scoped>

</style>
