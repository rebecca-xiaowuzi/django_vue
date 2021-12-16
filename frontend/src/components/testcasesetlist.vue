<template>
  <div>
  <el-form :inline="true" :model="searchtestcaseset" class="demo-form-inline">
    <el-form-item label="项目编号">
    <el-select v-model="searchtestcaseset.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
     <el-form-item label="用例集名称">
    <el-input v-model="searchtestcaseset.testcasesetName" placeholder="用例集名称"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchTestcaseSet">查询</el-button>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="addTestcaseSet">新增用例集</el-button>
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
      prop="testcasesetName"
      label="用例集名称">
    </el-table-column>
    <el-table-column
      prop="testcasesetCode"
      label="用例集Code">
    </el-table-column>
    <el-table-column
      prop="testcaselist"
      label="用例列表">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
<!--        <el-button type="text" size="small"  @click="updatetestcaseset(scope.row)">编辑</el-button>-->

 <el-dropdown trigger="click" @command="runtestcaseset">
   <el-button type="primary"  @click ="getenvironmentList(scope.row)">运行</el-button>
  <el-dropdown-menu slot="dropdown">
    <el-dropdown-item v-for="item in environmentlist" :command="beforeHandleCommand(scope.row,item.environmentName)" v-text="item.environmentName"></el-dropdown-item>
  </el-dropdown-menu>
</el-dropdown>
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
      searchtestcaseset: {
        projectCode: '',
        testcasesetName: ''
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
      this.searchTestcaseSet()
    },
  methods: {
    beforeHandleCommand(row,command){
      return {row,command}
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
    runtestcaseset(command){
      this.$http.post('TestCaseSet/RunTestCaseSet', {projectCode:command.row.projectCode, testcasesetCode:command.row.testcasesetCode, environmentName:command.command}).then(response => {
          return this.$message({message: response.data.msg, center: true})
      })

    },
    updatetestcaseset (row) {
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
    searchTestcaseSet () {
      this.$http.post('TestCaseSet/testcasesetlist', {projectCode: this.searchtestcaseset.projectCode, testcasesetName: this.searchtestcaseset.testcasesetName, page: this.page, pagesize: this.pagesize}).then(response => {
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
      this.searchTestcaseSet()
    },
    addTestcaseSet () {
      this.$router.push('/addtestcaseset')
    }
  }
}
</script>
<style scoped>

</style>
