<template>
    <el-form  :model="sql">
      <el-form-item label="sql名称">
    <el-input  v-model="sql.sqlname"></el-input>
  </el-form-item>
      <el-form-item label="前置需转换的数据">
         <el-table :data="sql.requesttransfer">
<el-table-column prop="name" label="key" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.name" :value="scope.row.name" placeholder="请输入key"></el-input>
                                </template>
                            </el-table-column>
<el-table-column  prop="value" label="内容" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.value" :value="scope.row.value" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
           <el-table-column label="操作" min-width="10%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delrequesttransfer(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(sql.requesttransfer.length-1)" size="mini" class="el-icon-plus" @click="addrequesttransfer"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
  <el-form-item label="sql列表">
   <el-select v-model="sql.sqlCode"  placeholder="sql列表">
       <el-option
      v-for="item in sqllist"
      :key="item.sqlCode"
      :label="item.sqlCode"
      :value="item.sqlCode">
    </el-option>
    </el-select>
  </el-form-item>
 <el-form-item label="环境列表">
  <el-select v-model="sql.environmentName"  placeholder="环境列表" @change="getsqlconnectlist">
       <el-option
      v-for="item in environmentlist"
      :key="item.environmentName"
      :label="item.environmentName"
      :value="item.environmentName">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="数据库连接列表">
  <el-select v-model="sql.sqlconnectCode"  placeholder="数据库连接列表">
       <el-option
      v-for="item in sqlconnectlist"
      :key="item.sqlconnectCode"
      :label="item.sqlconnectCode"
      :value="item.sqlconnectCode">
    </el-option>
    </el-select>
  </el-form-item>

<el-button  type="primary"  @click="runSql">运行</el-button>
<el-form-item label="sql执行结果">
   <el-input  type="textarea" autosize disabled v-model="sql.result"></el-input>
  </el-form-item>
       <el-form-item label="转换参数名称">
   <el-input  v-model="sql.responsetransfer"></el-input>
  </el-form-item>
    </el-form>

</template>

<script>
export default {
  props: {projectCode:String,sql_default:Object},
  data () {
    return {
      sql: {
        sqlCode: '',
        responsetransfer: '',
        requesttransfer: [{name: '', value: ''}],
        result: '',
        environmentName: '',
        sqlconnectCode: '',
        sqlname: ''
      },
      sqllist: [],
      sqlconnectlist: [],
      environmentlist: []
    }
  },
  created(){
    this.getsqllist(),
      this.getenvironmentList()

  },
  methods: {
    getsqldefault(){if (this.sql_default){
       this.sql= JSON.parse(JSON.stringify({...this.sql,...this.sql_default}))
      }},
    runSql () {
      var runsqlparam = {
        requesttransfer: '',
        sqlconnectCode: this.sql.sqlconnectCode,
        sqlCode: this.sql.sqlCode
      }
      // 处理requesttransfer数据格式--从数组转为字典
      var requesttransfernew = {}
      if ((this.sql.requesttransfer.length === 1) & (this.sql.requesttransfer[0].name === '') & (this.sql.requesttransfer[0].value === '')) {
        delete runsqlparam.requesttransfer
      } else {
        for (var i = 0, len = this.sql.requesttransfer.length; i < len; i++) {
          requesttransfernew[this.sql.requesttransfer[i]['name']] = this.sql.requesttransfer[i]['value']
        }
        runsqlparam['requesttransfer'] = requesttransfernew
      }
      this.$http.post('Sql/ExcuteSql', runsqlparam).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.sql.result = response.data.result
        }
      })
    },
    getsqllist () {
      this.$http.post('Sql/getsqllist', {}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.sqllist = response.data.data
          this.sql.sqlCode = response.data.data[0].sqlCode
          this.getsqldefault()

        }
      })
    },
    getsqlconnectlist () {
      this.$http.post('Sql/getsqlconnectlist', {environmentName: this.sql.environmentName, projectCode: this.projectCode}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.sqlconnectlist = response.data.data

          if (this.sqlconnectlist.length !== 0) {
            this.sql.sqlconnectCode = response.data.data[0].sqlconnectCode
          } else { this.sqlconnectCode = '' }
        }
      })
    },
    getenvironmentList () {
      var projectcode = this.projectCode
      this.$http.get(`Environment/getEnvironmentbyprojectcode?projectCode=${projectcode}`).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目环境下拉列表数据
          this.environmentlist = response.data.data
          // 环境下拉框设置默认值
          if (this.environmentlist.length !== 0) {
            this.sql.environmentName = response.data.data[0].environmentName
            this.getsqlconnectlist()
          } else { this.environmentName = '' }
        }
      })
    },
    addrequesttransfer () {
      let requesttransfer = {name: '', value: ''}
      this.sql.requesttransfer.push(requesttransfer)
    },
    delrequesttransfer (index) {
      this.sql.requesttransfer.splice(index, 1)
      if (this.sql.requesttransfer.length === 0) {
        this.sql.requesttransfer.push({name: '', value: ''})
      }
    }

  }
}
</script>

<style scoped>

</style>
