<template>
  <div>
  <el-form :inline="true" :model="searchvariable" class="demo-form-inline">
    <el-form-item label="项目编号">
    <el-select v-model="searchvariable.projectCode"  placeholder="项目编号" @change="getprojectlist">
       <el-option
      v-for="(item,index) in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="index">
    </el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="环境名称">
    <el-select v-model="searchvariable.environmentName" placeholder="环境名称">
       <el-option
      v-for="item in environments"
      :key="item.environmentName"
      :label="item.environmentName"
      :value="item.environmentName">
    </el-option>
    </el-select>
  </el-form-item>
     <el-form-item label="变量名称">
    <el-input v-model="searchvariable.variableName" placeholder="变量名称"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchVariable">查询</el-button>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="addVariable">新增变量</el-button>
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
      prop="environmentName"
      label="环境名称">
    </el-table-column>
    <el-table-column
      prop="variableName"
      label="变量名称">
    </el-table-column>
    <el-table-column
      prop="variable"
      label="变量值">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button type="text" size="small"  @click="updateproject(scope.row)">编辑</el-button>
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
      searchvariable: {
        projectCode: '',
        environmentName: '',
        variableName: ''
      },
      projectlist: this.getprojectlist(),
      environments: '',
      index: 0,
      tableData: [],
      total: 0,
      page: 1,
      pagesize: 10
    }
  },
  methods: {
    // 点击查询按钮查询变量信息
    searchVariable () {
      this.$http.post('Environment/getVariablelist', {variableName: this.searchvariable.variableName, environmentName: this.searchvariable.environmentName, projectCode: this.searchvariable.projectCode, page: this.page, pagesize: this.pagesize}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.tableData = response.data.data
          this.total = response.data.total
        }
      })
    },
    getprojectlist (val) {
      this.index = val
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
          // 项目下拉框设置默认值
          this.searchvariable.projectCode = response.data.data[this.index].projectCode
          // 判断项目下是否有环境变量 有 获取列表 给默认值
          if (response.data.data[this.index].environments.length !== 0) {
            this.environments = response.data.data[this.index].environments
            this.searchvariable.environmentName = response.data.data[this.index].environments[0].environmentName
            this.searchVariable()
          } else { this.searchvariable.environmentName = ''; this.tableData = []; this.environments = [] }// 无环境信息时，清空输入框数据
        }
      })
    },
    // 获取页数直接请求list接口
    handleCurrentChange (val) {
      this.page = val
      this.searchVariable()
    },
    addVariable () {
      this.$router.push('/addvariable')
    }

  }
}
</script>

<style scoped>

</style>
