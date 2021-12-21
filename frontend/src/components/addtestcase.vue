<template>
  <div class="row">
    <el-form  :model="testcase">
      <el-form-item label="项目编号">
    <el-select v-model="testcase.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
      </el-form-item>
       <el-form-item label="用例名称">
    <el-input  v-model="testcase.testcaseName"></el-input>
  </el-form-item>
       <el-form-item label="用例编号">
    <el-input  v-model="testcase.testcaseCode"></el-input>
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
          :key="index">
          <el-collapse-item :name="element.id">
            <template slot="title">
              <span>{{element.name}}</span>
              <i class="el-icon-circle-close" @click.stop="deleteItem(index)"></i>
            </template>
            <div ><component :is="element.type"  :ref="element.type" :projectCode="testcase.projectCode"></component> </div>
          </el-collapse-item>
        </el-collapse>
      </draggable>
    </div>
<el-button type="primary" @click="addtestcase">新增用例</el-button>
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
        projectCode: '',
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
      projectlist: this.projectList(),
      index: 0
    }
  },

  methods: {
    handleChange: function () {
    },
    deleteItem: function (index) {
      this.list2.splice(index, 1)
    },
    projectList () {
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
          // 项目下拉框设置默认值
          this.testcase.projectCode = response.data.data[0].projectCode
        }
      })
    },
    addtestcase () {
      var TestCaseDetail = []
     var child_api_number=0
        var child_sql_number=0
        var child_funcation_number=0
      for (var i = 0, len = this.list2.length; i < len; i++) {

        if (this.list2[i].type === 'childapi') {
          var testcasedetail_api = {}
          testcasedetail_api['type'] = 'API'
          testcasedetail_api['testcaseDetailOrder'] = i
          testcasedetail_api['testcaseDetailCode'] = this.$refs.childapi[child_api_number].api.apiCode
          testcasedetail_api['testcaseDetailName'] = this.$refs.childapi[child_api_number].api.apiname
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_api = {}
          if ((this.$refs.childapi[child_api_number].api.requesttransfer.length === 1) & (this.$refs.childapi[child_api_number].api.requesttransfer[0].name === '') & (this.$refs.childapi[child_api_number].api.requesttransfer[0].value === '')) {
          } else {
            for (var j = 0; j < this.$refs.childapi[child_api_number].api.requesttransfer.length; j++) {
              requesttransfer_api[this.$refs.childapi[child_api_number].api.requesttransfer[j]['name']] = this.$refs.childapi[child_api_number].api.requesttransfer[j]['value']
            }
            testcasedetail_api['requesttransfer'] = JSON.stringify(requesttransfer_api)
          }

          // responsetransfer--从数组转为字典
          var responsetransfer_api = {}
          if ((this.$refs.childapi[child_api_number].api.responsetransfer.length === 1) & (this.$refs.childapi[child_api_number].api.responsetransfer[0].name === '') & (this.$refs.childapi[child_api_number].api.responsetransfer[0].value === '')) {
          } else {
            for (var k = 0; k < this.$refs.childapi[child_api_number].api.responsetransfer.length; k++) {
              responsetransfer_api[this.$refs.childapi[child_api_number].api.responsetransfer[k]['name']] = this.$refs.childapi[child_api_number].api.responsetransfer[k]['value']
            }
            testcasedetail_api['responsetransfer'] = JSON.stringify(responsetransfer_api)
          }

          TestCaseDetail.push(testcasedetail_api)
          child_api_number=child_api_number+1
        } else if (this.list2[i].type === 'childsql') {
          var testcasedetail_sql = {}
          testcasedetail_sql['type'] = 'SQL'
          testcasedetail_sql['testcaseDetailOrder'] = i
          testcasedetail_sql['testcaseDetailCode'] = this.$refs.childsql[child_sql_number].sql.sqlCode
          testcasedetail_sql['testcaseDetailName'] = this.$refs.childsql[child_sql_number].sql.sqlname
          testcasedetail_sql['responsetransfer'] = this.$refs.childsql[child_sql_number].sql.responsetransfer
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_sql = {}
          if ((this.$refs.childsql[child_sql_number].sql.requesttransfer.length === 1) & (this.$refs.childsql[child_sql_number].sql.requesttransfer[0].name === '') & (this.$refs.childsql[child_sql_number].sql.requesttransfer[0].value === '')) {
          } else {
            for (var a = 0; a < this.$refs.childsql[child_sql_number].sql.requesttransfer.length; a++) {
              requesttransfer_sql[this.$refs.childsql[child_sql_number].sql.requesttransfer[a]['name']] = this.$refs.childsql[child_sql_number].sql.requesttransfer[a]['value']
            }
            testcasedetail_sql['requesttransfer'] = JSON.stringify(requesttransfer_sql)
          }


          TestCaseDetail.push(testcasedetail_sql)
          child_sql_number=child_sql_number+1
        } else if (this.list2[i].type === 'childfuncation') {
          var testcasedetail_funcation = {}
          testcasedetail_funcation['type'] = 'FUNCATION'
          testcasedetail_funcation['testcaseDetailOrder'] = i
          testcasedetail_funcation['testcaseDetailCode'] = this.$refs.childfuncation[child_funcation_number].funcation.funcation
          testcasedetail_funcation['testcaseDetailName'] = this.$refs.childfuncation[child_funcation_number].funcation.funcationname
          testcasedetail_funcation['responsetransfer'] = this.$refs.childfuncation[child_funcation_number].funcation.responsetransfer
          // 处理requesttransfer数据格式--从数组转为字典
          var requesttransfer_funcation = {}
          if ((this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer.length === 1) & (this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer[0].name === '') & (this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer[0].value === '')) {
          } else {
            for (var c = 0; c < this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer.length; c++) {
              requesttransfer_funcation[this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer[c]['name']] = this.$refs.childfuncation[child_funcation_number].funcation.requesttransfer[c]['value']
            }
            testcasedetail_funcation['requesttransfer'] = JSON.stringify(requesttransfer_funcation)
          }

          TestCaseDetail.push(testcasedetail_funcation)
          child_funcation_number=child_funcation_number+1
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
