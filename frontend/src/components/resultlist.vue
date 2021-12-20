<template>
  <div>
  <el-form :inline="true" :model="searchresult" class="demo-form-inline">
    <el-form-item label="项目编号">
    <el-select v-model="searchresult.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
     <el-form-item label="用例集编号">
    <el-input v-model="searchresult.testcasesetCode" placeholder="用例集编号"></el-input>
  </el-form-item>
    <el-form-item label="用例编号">
    <el-input v-model="searchresult.testcaseCode" placeholder="用例编号"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchResult">查询</el-button>
  </el-form-item>
</el-form>
  <div>
  <el-table
    :data="tableData"
    border>
    <el-table-column
      fixed
      prop="id"
      label="序号">
    </el-table-column>
    <el-table-column
      fixed
      prop="projectCode"
      label="项目编号">
    </el-table-column>
    <el-table-column
      prop="testcasesetCode"
      label="用例集编号">
    </el-table-column>
    <el-table-column
      prop="testcaseCode"
      label="用例编号">
    </el-table-column>
    <el-table-column
      prop="result"
      label="执行结果">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
   <el-button type="primary"  @click ="getresultdetail(scope.row)">详情</el-button>
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
      searchresult: {
        projectCode: '',
        testcasesetCode: '',
        testcaseCode:''
      },
      projectlist: this.projectList(),
      tableData: [],
      page: 1,
      pagesize: 10,
      total: 0


    }
  },
  created(){
      this.searchResult()
    },
  methods: {
    getresultdetail (row) {
      this.$router.push({path: '/resultdetail', query: { id: row.id}})
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
    searchResult () {
      this.$http.post('Result/ResultList', {projectCode: this.searchresult.projectCode, testcasesetCode: this.searchresult.testcasesetCode,testcaseCode: this.searchresult.testcaseCode, page: this.page, pagesize: this.pagesize}).then(response => {
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
      this.searchResult()
    }
  }
}
</script>
<style scoped>

</style>
