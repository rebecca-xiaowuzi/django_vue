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
      <h3>新增用例</h3>
      <draggable
        tag="el-collapse"
        class="dragArea list-group"
        :list="list2"
        group="comp"
        @change="change"
        >
        <el-collapse
          class="list-group-item left"
          v-for="(element,index) in list2"
          :key="index">
<!--          @change="handleChange"-->
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
    change: function (evt) {
      // if (evt.added) {
      //   this.count += 1
      //   const item = evt.added.element
      //   const idx = this.list2.findIndex(e => e.id === item.id)
      //   let temp = JSON.parse(JSON.stringify(this.list2))
      //   temp[idx].id = this.count
      //   this.list2 = temp
      // }
      // if (evt.moved) {
      //   const item = evt.moved.element
      //   const idx = this.list2.findIndex(e => e.id === item.id)
      //   let temp = JSON.parse(JSON.stringify(this.list2))
      //   temp[idx].id = this.count
      //   this.list2 = temp
      // }
    },
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
      for (var i = 0, len = this.list2.length; i < len; i++) {
        console.log(this.list2[i].type)
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
            for (var j = 0; j < this.$refs.childapi[0].api.requesttransfer.length; i++) {
              requesttransfer_api[this.$refs.childapi[0].api.requesttransfer[j]['name']] = this.$refs.childapi[0].api.requesttransfer[j]['value']
            }
            testcasedetail_api['requesttransfer'] = JSON.stringify(requesttransfer_api)
          }

          // responsetransfer--从数组转为字典
          var responsetransfer_api = {}
          if ((this.$refs.childapi[0].api.responsetransfer.length === 1) & (this.$refs.childapi[0].api.responsetransfer[0].name === '') & (this.$refs.childapi[0].api.responsetransfer[0].value === '')) {
          } else {
            for (var k = 0; k < this.$refs.childapi[0].api.responsetransfer.length; i++) {
              responsetransfer_api[this.$refs.childapi[0].api.responsetransfer[k]['name']] = this.$refs.childapi[0].api.responsetransfer[k]['value']
            }
            testcasedetail_api['responsetransfer'] = JSON.stringify(responsetransfer_api)
          }

          TestCaseDetail.push(testcasedetail_api)
          console.log(TestCaseDetail)
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
            for (var a = 0; a < this.$refs.childsql[0].sql.requesttransfer.length; i++) {
              requesttransfer_sql[this.$refs.childsql[0].sql.requesttransfer[a]['name']] = this.$refs.childsql[0].sql.requesttransfer[a]['value']
            }
            testcasedetail_sql['requesttransfer'] = JSON.stringify(requesttransfer_sql)
          }

          // 处理responsetransfer数据格式--从数组转为字典
          var responsetransfer_sql = {}
          if ((this.$refs.childsql[0].sql.responsetransfer.length === 1) & (this.$refs.childsql[0].sql.responsetransfer[0].name === '') & (this.$refs.childsql[0].sql.responsetransfer[0].value === '')) {
          } else {
            for (var b = 0; b < this.$refs.childsql[0].sql.responsetransfer.length; i++) {
              responsetransfer_sql[this.$refs.childsql[0].sql.responsetransfer[b]['name']] = this.$refs.childsql[0].sql.responsetransfer[b]['value']
            }
            testcasedetail_sql['responsetransfer'] = JSON.stringify(responsetransfer_sql)
          }

          TestCaseDetail.push(testcasedetail_sql)
          console.log(TestCaseDetail)
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
            for (var c = 0; c < this.$refs.childfuncation[0].funcation.requesttransfer.length; i++) {
              requesttransfer_funcation[this.$refs.childfuncation[0].funcation.requesttransfer[c]['name']] = this.$refs.childfuncation[0].funcation.requesttransfer[c]['value']
            }
            testcasedetail_funcation['requesttransfer'] = JSON.stringify(requesttransfer_funcation)
          }

          TestCaseDetail.push(testcasedetail_funcation)
          console.log(TestCaseDetail)
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
