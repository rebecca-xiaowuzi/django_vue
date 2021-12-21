<template>
  <div>
  <el-form :inline="true" :model="searchapi" class="demo-form-inline">
    <el-form-item label="项目编号">
    <el-select v-model="searchapi.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
     <el-form-item label="接口名称">
    <el-input v-model="searchapi.apiname" placeholder="接口名称"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="searchApi">查询</el-button>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="addApi">新增接口</el-button>
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
      prop="apiname"
      label="接口名称">
    </el-table-column>
    <el-table-column
      prop="apiCode"
      label="接口Code">
    </el-table-column>
    <el-table-column
      prop="apiAddress"
      label="接口地址">
    </el-table-column>
    <el-table-column
      prop="httpType"
      label="协议">
    </el-table-column>
    <el-table-column
      prop="requestType"
      label="请求方式">
    </el-table-column>
    <el-table-column
      prop="description"
      label="接口所属服务">
    </el-table-column>
    <el-table-column
      prop="status"
      label="接口状态">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="创建时间">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作">
      <template slot-scope="scope">
        <el-button type="text" size="small"  @click="updateapi(scope.row)">编辑</el-button>
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
      searchapi: {
        projectCode: '',
        apiname: ''
      },
      projectlist: this.projectList(),
      tableData: [],
      page: 1,
      pagesize: 10,
      total: 0
    }
  },
  created(){
      this.searchApi()
    },
  methods: {
    updateapi (row) {
      this.$router.push({path: '/updateapi', query: { projectCode: row.projectCode, apiCode: row.apiCode }})
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
    searchApi () {
      this.$http.post('api/Api/apilist', {projectCode: this.searchapi.projectCode, apiname: this.searchapi.apiname, page: this.page, pagesize: this.pagesize}).then(response => {
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
      this.searchApi()
    },
    addApi () {
      this.$router.push('/addapi')
    }
  }
}
</script>

<style scoped>

</style>
