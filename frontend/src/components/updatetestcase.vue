<template>
  <div class="row">
    <el-form  :model="testcase">
       <el-form-item label="项目编号">
   <el-input v-model="testcase.projectCode"  disabled>
    </el-input>
       </el-form-item>
       <el-form-item label="用例名称">
    <el-input  v-model="testcase.testcaseName"></el-input>
  </el-form-item>
       <el-form-item label="用例编号">
    <el-input  v-model="testcase.testcaseCode" disabled></el-input>
  </el-form-item>
       <el-form-item label="所属模块">
    <el-input  v-model="testcase.testcaseModel"></el-input>
  </el-form-item>
    <div class="col-5">
      <h3>用例详情</h3>
      <draggable
        tag="el-collapse"
        class="dragArea list-group"
        :list="list2"
        group="comp"
        >
        <el-collapse
          class="list-group-item left"
          v-for="(element,index) in list2"
          :key="index"
        >
          <el-collapse-item :name="element.id">
            <template slot="title">
              <span>{{element.name}}</span>
              <i class="el-icon-circle-close" @click.stop="deleteItem(index)"></i>
            </template>
            <div ><component :is="element.type"  :ref="element.type" :projectCode="testcase.projectCode" :api_default="api" :sql_default="sql" :funcation_default="funcation"></component> </div>
          </el-collapse-item>
        </el-collapse>
      </draggable>
    </div>
<el-button type="primary" @click="updatetestcase">更新用例</el-button>
    <el-button @click="cancel">取消</el-button>
          </el-form>
    <div class="col-5">
      <h3>可用组件列表</h3>
      <draggable
        class="dragArea list-group"
        :list="list1"
        :group="{ name: 'comp', pull: 'clone', put: false }"
      >
        <div class="list-group-item" v-for="element in list1" :key="element.type">{{ element.name }}</div>
      </draggable>
    </div>
  </div>
</template>
<script>
import draggable from 'vuedraggable'
import childsql from '../components/childsql'
import childfuncation from '../components/childfuncation'
import childapi from '../components/childapi'

export default {
  components: {
    draggable, childapi, childsql, childfuncation
  },
  data () {
    return {
      testcase: {
        projectCode: this.gettestcasedetail(),
        testcaseName: '',
        testcaseCode: '',
        testcaseModel: ''
      },
      list1: [
        {name: '接口', type: 'childapi'},
        {name: 'sql', type: 'childsql'},
        {name: '函数', type: 'childfuncation'}
      ],
      list2: [],
      activeNames: [],
      count: 0,
      index: 0,
      api: {},
      sql:{},
      funcation:{}

    }
  },

  methods: {
        // 获取详情展示
    gettestcasedetail () {
      this.$http.post('TestCase/GetTestcaseDetail', {projectCode: this.$route.query.projectCode, testcaseCode: this.$route.query.testcaseCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.testcase = response.data.data
        //  获取TestCaseDetail
          for (var i=0, len = response.data.data.TestCaseDetail.length; i < len; i++){
            if  (response.data.data.TestCaseDetail[i].type==='API'){
              //处理所有的接口返回的数据，显示在页面中
              this.api.apiCode=response.data.data.TestCaseDetail[i].testcaseDetailCode
              this.api.apiname=response.data.data.TestCaseDetail[i].testcaseDetailName
              if (response.data.data.TestCaseDetail[i].requesttransfer!=' '){
                var list_requesttransfer=[]
                var json_requesttransfer_api=JSON.parse(response.data.data.TestCaseDetail[i].requesttransfer)
                for (var requesttransfer_api in json_requesttransfer_api) {
                list_requesttransfer.push({name: requesttransfer_api, value: json_requesttransfer_api[requesttransfer_api]})
              }
              this.api.requesttransfer=list_requesttransfer
              }
              if (response.data.data.TestCaseDetail[i].responsetransfer!=' '){
                var list_responsetransfer=[]
                var json_responsetransfer_api=JSON.parse(response.data.data.TestCaseDetail[i].responsetransfer)
                for (var responsetransfer_api in json_responsetransfer_api) {
                list_responsetransfer.push({name: responsetransfer_api, value: json_responsetransfer_api[responsetransfer_api]})
              }
              this.api.responsetransfer=list_responsetransfer
              }
              this.list2.push({name: "接口", type: "childapi"})

            }
            else if (response.data.data.TestCaseDetail[i].type==='SQL') {
              this.sql.sqlCode=response.data.data.TestCaseDetail[i].testcaseDetailCode
              this.sql.sqlname=response.data.data.TestCaseDetail[i].testcaseDetailName
              if (response.data.data.TestCaseDetail[i].requesttransfer!=' '){
                var list_requesttransfer_sql=[]
                var json_requesttransfer_sql=JSON.parse(response.data.data.TestCaseDetail[i].requesttransfer)
                for (var requesttransfer_sql in json_requesttransfer_sql) {
                list_requesttransfer_sql.push({name: requesttransfer_sql, value: json_requesttransfer_sql[requesttransfer_sql]})
              }
              this.sql.requesttransfer=list_requesttransfer_sql
              }
              if (response.data.data.TestCaseDetail[i].responsetransfer!=' '){
                var list_responsetransfer_sql=[]
                var json_responsetransfer_sql=JSON.parse(response.data.data.TestCaseDetail[i].responsetransfer)
                for (var responsetransfer_sql in json_responsetransfer_sql) {
                list_responsetransfer_sql.push({name: responsetransfer_sql, value: json_responsetransfer_sql[responsetransfer_sql]})
              }
              this.sql.responsetransfer=list_responsetransfer_sql
              }
              this.list2.push({name: "sql", type: "childsql"})
            }
            else if (response.data.data.TestCaseDetail[i].type==='FUNCATION'){
              this.funcation.funcationname=response.data.data.TestCaseDetail[i].testcaseDetailName
              this.funcation.funcation=response.data.data.TestCaseDetail[i].testcaseDetailCode
              this.funcation.responsetransfer=response.data.data.TestCaseDetail[i].responsetransfer
              if (response.data.data.TestCaseDetail[i].requesttransfer!=' '){
                var list_requesttransfer_f=[]
                var json_requesttransfer_f=JSON.parse(response.data.data.TestCaseDetail[i].requesttransfer)
                for (var requesttransfer_f in json_requesttransfer_f) {
                list_requesttransfer_f.push({name: requesttransfer_f, value: json_requesttransfer_f[requesttransfer_f]})
              }
              this.funcation.requesttransfer=list_requesttransfer_f
              }
              this.list2.push({name: "函数", type: "childfuncation"})
            }
          }
        }
      })
    },
    handleChange: function () {
    },
    deleteItem: function (index) {
      this.list2.splice(index, 1)
    },
    updatetestcase () {
      var TestCaseDetail = []
      for (var i = 0, len = this.list2.length; i < len; i++) {
        if (this.list2[i].type === 'childapi') {
          var testcasedetail_api = {}
          testcasedetail_api['type'] = 'API'
          testcasedetail_api['testcaseDetailOrder'] = i
          testcasedetail_api['testcaseDetailCode'] = this.$refs.childapi[0].api.apiCode
          testcasedetail_api['testcaseDetailName'] = this.$refs.childapi[0].api.apiname
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_api = {}
          if ((this.$refs.childapi[0].api.requesttransfer.length === 1) & (this.$refs.childapi[0].api.requesttransfer[0].name === '') & (this.$refs.childapi[0].api.requesttransfer[0].value === '')) {
          } else {
            for (var j = 0; j < this.$refs.childapi[0].api.requesttransfer.length; j++) {
              requesttransfer_api[this.$refs.childapi[0].api.requesttransfer[j]['name']] = this.$refs.childapi[0].api.requesttransfer[j]['value']
            }
            testcasedetail_api['requesttransfer'] = JSON.stringify(requesttransfer_api)
          }

          // responsetransfer--从数组转为字典
          var responsetransfer_api = {}
          if ((this.$refs.childapi[0].api.responsetransfer.length === 1) & (this.$refs.childapi[0].api.responsetransfer[0].name === '') & (this.$refs.childapi[0].api.responsetransfer[0].value === '')) {
          } else {
            for (var k = 0; k < this.$refs.childapi[0].api.responsetransfer.length; k++) {
              responsetransfer_api[this.$refs.childapi[0].api.responsetransfer[k]['name']] = this.$refs.childapi[0].api.responsetransfer[k]['value']
            }
            testcasedetail_api['responsetransfer'] = JSON.stringify(responsetransfer_api)
          }

          TestCaseDetail.push(testcasedetail_api)
        } else if (this.list2[i].type === 'childsql') {
          var testcasedetail_sql = {}
          testcasedetail_sql['type'] = 'SQL'
          testcasedetail_sql['testcaseDetailOrder'] = i
          testcasedetail_sql['testcaseDetailCode'] = this.$refs.childsql[0].sql.sqlCode
          testcasedetail_sql['testcaseDetailName'] = this.$refs.childsql[0].sql.sqlname
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_sql = {}
          if ((this.$refs.childsql[0].sql.requesttransfer.length === 1) & (this.$refs.childsql[0].sql.requesttransfer[0].name === '') & (this.$refs.childsql[0].sql.requesttransfer[0].value === '')) {
          } else {
            for (var a = 0; a < this.$refs.childsql[0].sql.requesttransfer.length; a++) {
              requesttransfer_sql[this.$refs.childsql[0].sql.requesttransfer[a]['name']] = this.$refs.childsql[0].sql.requesttransfer[a]['value']
            }
            testcasedetail_sql['requesttransfer'] = JSON.stringify(requesttransfer_sql)
          }

          // 处理responsetransfer数据格式--从数组转为字典
          var responsetransfer_sql = {}
          if ((this.$refs.childsql[0].sql.responsetransfer.length === 1) & (this.$refs.childsql[0].sql.responsetransfer[0].name === '') & (this.$refs.childsql[0].sql.responsetransfer[0].value === '')) {
          } else {
            for (var b = 0; b < this.$refs.childsql[0].sql.responsetransfer.length; b++) {
              responsetransfer_sql[this.$refs.childsql[0].sql.responsetransfer[b]['name']] = this.$refs.childsql[0].sql.responsetransfer[b]['value']
            }
            testcasedetail_sql['responsetransfer'] = JSON.stringify(responsetransfer_sql)
          }

          TestCaseDetail.push(testcasedetail_sql)
        } else if (this.list2[i].type === 'childfuncation') {
          var testcasedetail_funcation = {}
          testcasedetail_funcation['type'] = 'FUNCATION'
          testcasedetail_funcation['testcaseDetailOrder'] = i
          testcasedetail_funcation['testcaseDetailCode'] = this.$refs.childfuncation[0].funcation.funcation
          testcasedetail_funcation['testcaseDetailName'] = this.$refs.childfuncation[0].funcation.funcationname
          testcasedetail_funcation['responsetransfer'] = this.$refs.childfuncation[0].funcation.responsetransfer
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_funcation = {}
          if ((this.$refs.childfuncation[0].funcation.requesttransfer.length === 1) & (this.$refs.childfuncation[0].funcation.requesttransfer[0].name === '') & (this.$refs.childfuncation[0].funcation.requesttransfer[0].value === '')) {
          } else {
            for (var c = 0; c < this.$refs.childfuncation[0].funcation.requesttransfer.length; c++) {
              requesttransfer_funcation[this.$refs.childfuncation[0].funcation.requesttransfer[c]['name']] = this.$refs.childfuncation[0].funcation.requesttransfer[c]['value']
            }
            testcasedetail_funcation['requesttransfer'] = JSON.stringify(requesttransfer_funcation)
          }

          TestCaseDetail.push(testcasedetail_funcation)
        }
      }
      var testcase = {
        projectCode: this.testcase.projectCode,
        testcaseName: this.testcase.testcaseName,
        testcaseCode: this.testcase.testcaseCode,
        testcaseModel: this.testcase.testcaseModel,
        TestCaseDetail
      }

      this.$http.post('TestCase/AddTestCase', testcase).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.$router.push('/testcaselist')
        }
      })
    },
    cancel () {
      this.$router.push('/testcaselist')
    }
  }
}
</script>
<style scoped>

</style>
