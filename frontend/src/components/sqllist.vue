<template>
  <div>
  <el-form :inline="true" :model="searchsql" class="demo-form-inline">
     <el-form-item label="sql名称">
    <el-input v-model="searchsql.sqlName" placeholder="sql名称"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchSql">查询</el-button>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="addsql">新增sql</el-button>
  </el-form-item>
</el-form>
  <div>
  <el-table
    :data="tableData"
    border>
    <el-table-column
      prop="sqlName"
      label="sql名称">
    </el-table-column>
    <el-table-column
      prop="sqlCode"
      label="sql编号">
    </el-table-column>
    <el-table-column
      prop="sql"
      label="sql">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button type="text" size="small"  @click="updatesql(scope.row)">编辑</el-button>
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
      searchsql: {
        sqlName: ''
      },
      tableData: [],
      total: 0,
      page: 1,
      pagesize: 10
    }
  },
  created(){
      this.searchSql()
    },
  methods: {
    // 点击查询按钮查询变量信息
    searchSql () {
      this.$http.post('Sql/getsqllist', {sqlName: this.searchsql.sqlName, page: this.page, pagesize: this.pagesize}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.tableData = response.data.data
          this.total = response.data.total
        }
      })
    },
    // 获取页数直接请求list接口
    handleCurrentChange (val) {
      this.page = val
      this.searchsql()
    },
    addsql () {
      this.$router.push('/addsql')
    },
    updatesql (row) {
      this.$router.push({path: '/updateConnectsql', query: {projectCode: row.projectCode, environmentName: row.environmentName, sqlconnectCode: row.sqlconnectCode}})
    }

  }
}
</script>

<style scoped>

</style>
