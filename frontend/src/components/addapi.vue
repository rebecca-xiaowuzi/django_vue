<template>
<<<<<<< HEAD
  <div>
    <el-form  :model="addapi">
  <el-form-item label="项目编号">
   <el-select v-model="addapi.projectCode"  placeholder="项目编号">
       <el-option
      v-for="item in projectlist"
      :key="item.projectCode"
      :label="item.projectCode"
      :value="item.projectCode">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="接口名称">
    <el-input  v-model="addapi.apiname"></el-input>
  </el-form-item>
       <el-form-item label="接口编号">
    <el-input  v-model="addapi.apiCode"></el-input>
  </el-form-item>
       <el-form-item label="httpType">
    <el-select v-model="addapi.httpType"  placeholder="httpType">
       <el-option
      v-for="item in httpTypelist"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="请求方式">
    <el-select v-model="addapi.requestType"  placeholder="请求方式">
       <el-option
      v-for="item in requestTypelist"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="接口地址">
    <el-input  v-model="addapi.apiAddress"></el-input>
  </el-form-item>
       <el-form-item label="接口描述">
    <el-input  v-model="addapi.description"></el-input>
  </el-form-item>
       <el-form-item label="接口状态">
    <el-checkbox v-model="addapi.status">启用</el-checkbox>
  </el-form-item>
       <el-form-item label="请求头信息">
         <el-table :data="addapi.apiHead">
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
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delHead(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(addapi.apiHead.length-1)" size="mini" class="el-icon-plus" @click="addHead"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
      <el-form-item label="参数格式">
    <el-select v-model="addapi.requestParameterType" placeholder="参数格式"  @change="paramsinit">
       <el-option
      v-for="item in requestParameterTypeList"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="请求参数" v-if="this.addapi.requestParameterType !== 'no-params'">
         <el-table :data="addapi.ApiRequestParam" v-if="this.addapi.requestParameterType === 'form-data'">
<el-table-column   prop="name" label="参数名称" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入参数名称"></el-input>
                                </template>
                            </el-table-column>
<el-table-column  prop="value" label="参数值" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
           <el-table-column label="操作" min-width="10%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delParam(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(addapi.ApiRequestParam.length-1)" size="mini" class="el-icon-plus" @click="addParam"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
         <el-input type="textarea" autosize v-model="addapi.ApiRequestParam" v-else-if="this.addapi.requestParameterType === 'raw'"></el-input>
  </el-form-item>
<!--       <el-form-item label="选择调试环境">-->
<!--   <el-select v-model="environmentName"  placeholder="选择调试环境">-->
<!--       <el-option-->
<!--      v-for="item in environmentlist"-->
<!--      :key="item.environmentName"-->
<!--      :label="item.environmentName"-->
<!--      :value="item.environmentName">-->
<!--    </el-option>-->
<!--    </el-select>-->
<!--  </el-form-item>-->
<!--      <el-form-item>-->
<!--          <el-button type="primary" @click="runApi">运行接口</el-button>-->
<!--        </el-form-item>-->
<!--      <el-form-item>-->
<!--          <el-input type="textarea" autosize v-model="response"></el-input>-->
<!--        </el-form-item>-->
      <el-form-item>
    <el-button type="primary" @click="addApi">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
=======

>>>>>>> origin/master
</template>

<script>
export default {
<<<<<<< HEAD
  data () {
    return {
      addapi: {
        projectCode: '',
        apiname: '',
        apiCode: '',
        httpType: '',
        requestType: '',
        apiAddress: '',
        description: '',
        status: true,
        apiHead: [{name: '', value: ''}],
        requestParameterType: '',
        ApiRequestParam: [{name: '', value: ''}]
      },
      projectlist: this.projectList(),
      httpTypelist: this.getallType(),
      requestTypelist: [],
      requestParameterTypeList: []
    }
  },
  methods: {
    projectList () {
      this.$http.get('Project/getProjects').then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目下拉列表数据
          this.projectlist = response.data.data
          // 项目下拉框设置默认值
          this.addapi.projectCode = response.data.data[0].projectCode
        }
      })
    },
    getallType () {
      this.$http.get('Api/getallType').then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          // 获取项目下拉列表数据
          this.httpTypelist = response.data['httpType']
          this.requestTypelist = response.data['requestType']
          this.requestParameterTypeList = response.data['requestParameterType']
          // 项目下拉框设置默认值
          this.addapi.httpType = this.httpTypelist[0][0]
          this.addapi.requestType = this.requestTypelist[0][0]
          this.addapi.requestParameterType = this.requestParameterTypeList[0][0]
        }
      })
    },
    addApi () {
      var addapiparam = {
        projectCode: this.addapi.projectCode,
        apiname: this.addapi.apiname,
        apiCode: this.addapi.apiCode,
        httpType: this.addapi.httpType,
        requestType: this.addapi.requestType,
        apiAddress: this.addapi.apiAddress,
        description: this.addapi.description,
        status: this.addapi.status,
        apiHead: '',
        requestParameterType: this.addapi.requestParameterType,
        ApiRequestParam: ''
      }
      // 处理apihead数据格式--从数组转为字典
      var apiHeadnew = {}
      if ((this.addapi.apiHead.length === 1) & (this.addapi.apiHead[0].name === '') & (this.addapi.apiHead[0].value === '')) {
        delete addapiparam.apiHead
      } else {
        for (var i = 0, len = this.addapi.apiHead.length; i < len; i++) {
          apiHeadnew[this.addapi.apiHead[i]['name']] = this.addapi.apiHead[i]['value']
        }
        addapiparam['apiHead'] = apiHeadnew
      }
      // 处理apiparams的数据格式
      // form-data时处理数据方式
      var apiParamnew = {}
      if (this.addapi.requestParameterType === 'form-data') {
        if ((this.addapi.ApiRequestParam.length === 1) & (this.addapi.ApiRequestParam[0].name === '') & (this.addapi.ApiRequestParam[0].value === '')) {
          delete addapiparam.ApiRequestParam
        } else {
          for (var j = 0, lens = this.addapi.ApiRequestParam.length; j < lens; j++) {
            apiParamnew[this.addapi.ApiRequestParam[j]['name']] = this.addapi.ApiRequestParam[j]['value']
          }
          addapiparam['ApiRequestParam'] = apiParamnew
        }
      }
      // no-params时处理数据方式
      if (this.addapi.requestParameterType === 'no-params') {
        delete addapiparam.ApiRequestParam
      }
      // raw时处理数据方式
      if (this.addapi.requestParameterType === 'raw') {
        if (this.addapi.ApiRequestParam === '') { delete addapiparam.ApiRequestParam } else {
          apiParamnew = this.addapi.ApiRequestParam
          addapiparam['ApiRequestParam'] = apiParamnew
        }
      }

      this.$http.post('Api/addApi', addapiparam).then(response => {
        if (response.data.code !== '9999') {
          // 处理apihead的数据格式--从字典转为数组

          if (!addapiparam.hasOwnProperty('apiHead')) {
            this.addapi.apiHead = [{name: '', value: ''}]
          } else {
            var apiHeadarray = []
            for (var key in addapiparam.apiHead) {
              apiHeadarray.push({name: key, value: addapiparam.apiHead[key]})
            }
            this.addapi.apiHead = apiHeadarray
          }
          // 处理apiparams的数据格式--从字典转为数组
          // form-data时处理数据方式
          if (this.addapi.requestParameterType === 'form-data') {
            if (!addapiparam.hasOwnProperty('ApiRequestParam')) {
              this.addapi.ApiRequestParam = [{name: '', value: ''}]
            } else {
              var apiParamarray = []
              for (var key2 in addapiparam.ApiRequestParam) {
                apiParamarray.push({name: key2, value: addapiparam.ApiRequestParam[key2]})
              }
              this.addapi.ApiRequestParam = apiParamarray
            }
          }
          // no-params时处理数据方式
          // if (this.addapi.requestParameterType === 'no-params') {
          //   this.addapi.ApiRequestParam = [{name: '', value: ''}]
          // }
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.$router.push('/apilist')
        }
      })
    },
    cancel () {
      this.$router.push('/apilist')
    },
    addHead () {
      let headers = {name: '', value: ''}
      this.addapi.apiHead.push(headers)
    },
    delHead (index) {
      this.addapi.apiHead.splice(index, 1)
      if (this.addapi.apiHead.length === 0) {
        this.addapi.apiHead.push({name: '', value: ''})
      }
    },
    addParam () {
      let params = {name: '', value: ''}
      this.addapi.ApiRequestParam.push(params)
    },
    delParam (index) {
      this.addapi.ApiRequestParam.splice(index, 1)
      if (this.addapi.ApiRequestParam.length === 0) {
        this.addapi.ApiRequestParam.push({name: '', value: ''})
      }
    },
    // 下拉框切换时，重置请求参数
    paramsinit () {
      if (this.addapi.requestParameterType === 'form-data') { this.addapi.ApiRequestParam = [{name: '', value: ''}] }
      if (this.addapi.requestParameterType === 'raw') { this.addapi.ApiRequestParam = '' }
      if (this.addapi.requestParameterType === 'no-params') { this.addapi.ApiRequestParam = '' }
    }
    // runApi () {
    //   let runapiparams = this.addapi
    //   runapiparams['environmentName'] = this.environmentName
    //   this.$http.post('Api/runApi', runapiparams).then(response => {
    //     if (response.data.code !== '9999') {
    //       return this.$message.error({message: response.data.msg, center: true})
    //     } else {
    //       this.response = response
    //     }
    //   })
    // },
    // getenvironmentList () {
    //   var projectcode = this.addapi.projectCode
    //   this.$http.get(`Environment/getEnvironmentbyprojectcode?projectCode=${projectcode}`).then(response => {
    //     if (response.data.code !== '9999') {
    //       return this.$message.error({message: response.data.msg, center: true})
    //     } else {
    //       // 获取项目环境下拉列表数据
    //       this.environmentlist = response.data.data
    //       // 环境下拉框设置默认值
    //       if (this.environmentlist.length !== 0) {
    //         this.environmentName = response.data.data[0].environmentName
    //       } else { this.environmentName = '' }
    //     }
    //   })
    // }
  }
=======
  name: 'addapi'
>>>>>>> origin/master
}
</script>

<style scoped>

</style>
