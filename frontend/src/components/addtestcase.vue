<template>
  <div class="row">
    <el-form  :model="testcase">
      <el-form-item label="项目编号">
    <el-select v-model="testcase.projectCode"  placeholder="项目编号">
       <el-option
      v-for="(item,index) in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="index">
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
          :key="index"
          v-model="activeNames"
          @change="handleChange"
        >
          <el-collapse-item :name="element.id">
            <template slot="title">
              <span>{{element.name}}</span>
              <i class="el-icon-circle-close" @click.stop="deleteItem(index)"></i>
            </template>
            <div ><component :is="element.type" :ref="element.type"></component> </div>
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
import draggable from "vuedraggable";
import childsql from '../components/childsql'
import childfuncation from '../components/childfuncation'
import childapi from '../components/childapi'

export default {
  components: {
    draggable, childapi, childsql, childfuncation
  },
  data() {
    return {
      testcase: {
        projectCode: "",
        testcaseName: "",
        testcaseCode: "",
        testcaseModel: ""
      },
      list1: [
        {name: "接口", type: "childapi"},
        {name: "sql", type: "childsql"},
        {name: "函数", type: "childfuncation"}
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
      if (evt.added) {
        this.count += 1
        const item = evt.added.element
        const idx = this.list2.findIndex(e => e.id === item.id)
        let temp = JSON.parse(JSON.stringify(this.list2))
        temp[idx].id = this.count
        this.list2 = temp
      }
      if (evt.moved) {
        const item = evt.moved.element
        const idx = this.list2.findIndex(e => e.id === item.id)
        let temp = JSON.parse(JSON.stringify(this.list2))
        temp[idx].id = this.count
        this.list2 = temp
      }
    },
    handleChange: function () {
      console.log("fffffffffffffffffffffffffffffffffffffffff")
    },
    deleteItem: function (index) {
      this.list2.splice(index, 1)
      console.log(this.list2)
    },
    projectList() {
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
    addtestcase() {
      var TestCaseDetail=[]
      for (var i = 0, len = this.list2.length; i < len; i++) {
        if (this.list2[i].type = "chilapi") {
              var testcasedetail_api={}
               testcasedetail_api['type']="API"
          testcasedetail_api['testcaseDetailOrder']=i
          testcasedetail_api['testcaseDetailCode']=this.$refs.chilapi.apiCode
           testcasedetail_api['testcaseDetailName']=this.$refs.chilapi.name
           // 处理requesttransfer数据格式--从数组转为字典
      var requesttransfer_api = {}
      if ((this.$refs.chilapi.requesttransfer.length === 1) & (this.$refs.chilapi.requesttransfer[0].name === '') & (this.$refs.chilapi.requesttransfer[0].value === '')) {
        pass
      } else {
        for (var i = 0, len = this.$refs.chilapi.requesttransfer.length; i < len; i++) {
          requesttransfer_api[this.$refs.chilapi.requesttransfer[i]['name']] = this.$refs.chilapi.requesttransfer[i]['value']

        }}
      testcasedetail_api['requesttransfer']=requesttransfer_api
          // 处理requesttransfer数据格式--从数组转为字典
      var responsetransfer_api = {}
      if ((this.$refs.chilapi.responsetransfer.length === 1) & (this.$refs.chilapi.responsetransfer[0].name === '') & (this.$refs.chilapi.responsetransfer[0].value === '')) {
        pass
      } else {
        for (var i = 0, len = this.$refs.chilapi.responsetransfer.length; i < len; i++) {
          responsetransfer_api[this.$refs.chilapi.responsetransfer[i]['name']] = this.$refs.chilapi.responsetransfer[i]['value']

        }}
      testcasedetail_api['responsetransfer']=responsetransfer_api
              TestCaseDetail.push()
          console.log(TestCaseDetail)
        }

      }


    }
  }
}
</script>
<style scoped>

</style>
