<template>
  <div>
    <el-form  :model="api">
        <el-form-item label="接口名称">
    <el-input  v-model="api.apiname"></el-input>
  </el-form-item>
      <el-form-item label="前置需转换的数据">
         <el-table :data="api.requesttransfer">
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
                                    <el-button v-if="scope.$index===(api.requesttransfer.length-1)" size="mini" class="el-icon-plus" @click="addrequesttransfer"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
  <el-form-item label="接口列表">
   <el-select v-model="api.apiCode"  placeholder="接口列表"  @change="getapidetail">
       <el-option
      v-for="item in apilist"
      :key="item.apiCode"
      :label="item.apiCode"
      :value="item.apiCode">
    </el-option>
    </el-select>
  </el-form-item>

      <el-form-item>
        <el-descriptions   :column="1"  >
          <el-descriptions-item label="api描述">{{apidetail.description}}</el-descriptions-item>
          <el-descriptions-item label="api地址" >{{apidetail.apiAddress}}</el-descriptions-item>
  <el-descriptions-item label="httpType">{{apidetail.httpType}}</el-descriptions-item>
  <el-descriptions-item label="请求方式">{{apidetail.requestType}}</el-descriptions-item>
  <el-descriptions-item label="请求头信息" >{{apidetail.apiHead}}</el-descriptions-item>
  <el-descriptions-item label="参数格式">{{apidetail.requestParameterType}}</el-descriptions-item>
          <el-descriptions-item label="参数信息" >{{apidetail.ApiRequestParam}}</el-descriptions-item>

</el-descriptions>
        </el-form-item>
      <el-form-item><el-button type="primary" @click="drawerclick"  style="margin-left: 16px;">运行调试</el-button>
        <el-drawer title="请求详情信息" :visible.sync="drawer">
  <el-select v-model="api.environmentName"  placeholder="环境列表">
       <el-option
      v-for="item in environmentlist"
      :key="item.environmentName"
      :label="item.environmentName"
      :value="item.environmentName">
    </el-option>
    </el-select>
<el-button  type="primary"  @click="runApi">运行</el-button>
          <el-descriptions   :column="1"  >
            <el-descriptions-item label="转换数据" >{{responsedetail.requesttransfer}}</el-descriptions-item>
          <el-descriptions-item label="api地址" >{{responsedetail.request_url}}</el-descriptions-item>
  <el-descriptions-item label="请求方式">{{responsedetail.request_method}}</el-descriptions-item>
  <el-descriptions-item label="请求头信息" >{{responsedetail.request_heads}}</el-descriptions-item>
          <el-descriptions-item label="参数信息" >{{responsedetail.request_params}}</el-descriptions-item>
            <el-descriptions-item label="响应码">{{responsedetail.response_code}}</el-descriptions-item>
            <el-descriptions-item label="响应信息">{{responsedetail.response}}</el-descriptions-item>

</el-descriptions>
</el-drawer>
      </el-form-item>

       <el-form-item label="后置需转换的数据">
         <el-table :data="api.responsetransfer">
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
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delresponsetransfer(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(api.responsetransfer.length-1)" size="mini" class="el-icon-plus" @click="addresponsetransfer"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
    </el-form>
  </div>

</template>

<script>
export default {
  props: {projectCode:String,api_default:Object},
  data () {
    return {
      api: {
        apiCode: '',
        responsetransfer: [{name: '', value: ''}],
        requesttransfer: [{name: '', value: ''}],
        environmentName: '',
        apiname: ''
      },
      apilist: [],
      apidetail: {
        httpType: '',
        requestType: '',
        apiAddress: '',
        ApiRequestParam: '',
        apiHead: '',
        description: '',
        requestParameterType: ''
      },
      drawer: false,
      environmentlist: [],
      responsedetail: {
        requesttransfer: {},
        request_url: '',
        request_method: '',
        request_heads: '',
        response_code: '',
        response: '',
        request_params: ''
      }
    }
  },
  created(){
    this.apiList()
    this.getenvironmentList()
  },
  methods: {
    drawerclick () {
      this.drawer = true
    },
     getapidefault(){
      if (this.api_default){
       this.api= JSON.parse(JSON.stringify({...this.api,...this.api_default}))
        // this.getapidetail()
      }
     },
    runApi () {
      var runapiparam = {
        projectCode: this.projectCode,
        environmentName: this.api.environmentName,
        apiCode: this.api.apiCode,
        requesttransfer: ''
      }
      // 处理requesttransfer数据格式--从数组转为字典
      var requesttransfernew = {}
      if ((this.api.requesttransfer.length === 1) & (this.api.requesttransfer[0].name === '') & (this.api.requesttransfer[0].value === '')) {
        delete runapiparam.requesttransfer
      } else {
        for (var i = 0, len = this.api.requesttransfer.length; i < len; i++) {
          requesttransfernew[this.api.requesttransfer[i]['name']] = this.api.requesttransfer[i]['value']
        }
        runapiparam['requesttransfer'] = requesttransfernew
        this.responsedetail.requesttransfer = requesttransfernew
      }
      this.$http.post('Api/runApi', runapiparam).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.responsedetail.request_url = response.data.request_url
          this.responsedetail.request_method = response.data.request_method
          this.responsedetail.response_code = response.data.response_code
          this.responsedetail.request_params = response.data.request_params
          this.responsedetail.response = response.data.response
          this.responsedetail.request_heads = response.data.request_heads
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
            this.api.environmentName = response.data.data[0].environmentName
          } else { this.environmentName = '' }
        }
      })
    },
    getapidetail () {
      this.$http.post('Api/GetApiDetail', {projectCode: this.projectCode, apiCode: this.api.apiCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.apidetail = response.data.data
        }
      })
    },
    apiList () {
      this.$http.get('Api/getapilistByprojectcode', {params: {projectCode: this.projectCode}}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else {
          this.apilist = response.data.data
          this.api.apiCode = response.data.data[0].apiCode
          this.getapidefault()
          this.getapidetail()
        }
      })



    },
    addresponsetransfer () {
      let responsetransfer = {name: '', value: ''}
      this.api.responsetransfer.push(responsetransfer)
    },
    delresponsetransfer (index) {
      this.api.responsetransfer.splice(index, 1)
      if (this.api.responsetransfer.length === 0) {
        this.api.responsetransfer.push({name: '', value: ''})
      }
    },
    addrequesttransfer () {
      let requesttransfer = {name: '', value: ''}
      this.api.requesttransfer.push(requesttransfer)
    },
    delrequesttransfer (index) {
      this.api.requesttransfer.splice(index, 1)
      if (this.api.requesttransfer.length === 0) {
        this.api.requesttransfer.push({name: '', value: ''})
      }
    }
  }
}
</script>

<style scoped>

</style>
