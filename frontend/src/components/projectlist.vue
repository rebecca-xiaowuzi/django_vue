<template>
  <div>
  <div>
  <el-button type="primary" @click="addproject">新建项目</el-button>
  </div>
  <div>
  <el-table
    :data="tableData"
    border>
    <el-table-column
      fixed
      prop="id"
      label="项目id">
    </el-table-column>
    <el-table-column
      prop="projectName"
      label="项目名称">
    </el-table-column>
    <el-table-column
      prop="projectCode"
      label="项目编号">
    </el-table-column>
    <el-table-column
      prop="projectDescription"
      label="项目描述">
    </el-table-column>
    <el-table-column
      prop="users"
      label="项目用户">
    </el-table-column>
    <el-table-column
      prop="environments"
      label="项目环境">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button  type="text" size="small" @click="projectdetail(scope.row)">查看</el-button>
        <el-button type="text" size="small"  @click="updateproject(scope.row)">编辑</el-button>
        <el-button type="text" size="small"  @click="addenvironment(scope.row)">添加环境信息</el-button>
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
  methods: {
    // 获取页数直接请求list接口
    handleCurrentChange (val) {
      this.$http.get(`Project/getProjects?pagesize=10&page=${val}`).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.tableData = response.data.data
          this.total = response.data.total
        }
      })
    },
    addproject () {
      this.$router.push('/addproject')
    },
    updateproject (row) {
      this.$router.push({path: '/updateproject', query: {projectCode: row.projectCode, projectName: row.projectName, projectDescription: row.projectDescription, users: row.users}})
    },
    addenvironment (row) {
      this.$router.push({path: '/addenvironment', query: {projectCode: row.projectCode}})
    },
    projectdetail (row) {
      this.$router.push({path: '/projectdetail', query: {projectCode: row.projectCode, projectName: row.projectName, projectDescription: row.projectDescription, users: row.users, environments: row.environments}})
    }
    // 暂未实现
    // deleteuser (row) {
    //   this.$confirm('此操作将删除该用户, 是否继续?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning',
    //     center: true
    //   }).then(() => {
    //     this.$http.post('User/deleteUser', {phone: row.phone}).then(response => {
    //       if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
    //         this.$message({
    //           type: 'success',
    //           message: '删除成功!'
    //         })
    //       }
    //     })
    //     this.handleCurrentChange(1)
    //   })
    // }
  },
  data () {
    return {
      tableData: this.handleCurrentChange(1),
      total: 0
    }
  }
}
</script>

<style scoped>

</style>
