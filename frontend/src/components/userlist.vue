<template>
  <div>
  <div>
  <el-button type="primary" @click="adduser">新建用户</el-button>
  </div>
  <div>
  <el-table
    :data="tableData"
    border>
    <el-table-column
      fixed
      prop="id"
      label="用户id">
    </el-table-column>
    <el-table-column
      prop="phone"
      label="电话">
    </el-table-column>
    <el-table-column
      prop="email"
      label="邮箱">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button  type="text" size="small">查看</el-button>
        <el-button type="text" size="small"  @click="updateuser(scope.row)">编辑</el-button>
        <el-button type="text" size="small"   @click="deleteuser(scope.row)">删除</el-button>
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
      this.$http.get(`User/getUsers?pagesize=10&page=${val}`).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.tableData = response.data.data
          this.total = response.data.total
        }
      })
    },
    adduser () {
      this.$router.push('/adduser')
    },
    updateuser (row) {
      this.$router.push({path: '/updateuser', query: {phone: row.phone, email: row.email}})
    },
    deleteuser (row) {
      this.$confirm('此操作将删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        this.$http.post('User/deleteUser', {phone: row.phone}).then(response => {
          if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
          }
        })
        this.handleCurrentChange(1)
      })
    }
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
