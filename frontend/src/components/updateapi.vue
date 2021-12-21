<template>
  <div>
    <el-form  :model="updateapi">
  <el-form-item label="项目编号">
   <el-input v-model="updateapi.projectCode"  disabled>
    </el-input>
  </el-form-item>
       <el-form-item label="接口名称">
    <el-input  v-model="updateapi.apiname"></el-input>
  </el-form-item>
       <el-form-item label="接口编号" >
    <el-input  v-model="updateapi.apiCode" disabled></el-input>
  </el-form-item>
       <el-form-item label="httpType">
    <el-select v-model="updateapi.httpType"  placeholder="httpType">
       <el-option
      v-for="item in httpTypelist"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="请求方式">
    <el-select v-model="updateapi.requestType"  placeholder="请求方式">
       <el-option
      v-for="item in requestTypelist"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="接口地址">
    <el-input  v-model="updateapi.apiAddress"></el-input>
  </el-form-item>
       <el-form-item label="接口所属服务">
    <el-input  v-model="updateapi.description"></el-input>
  </el-form-item>
       <el-form-item label="接口状态">
    <el-checkbox v-model="updateapi.status">启用</el-checkbox>
  </el-form-item>
       <el-form-item label="请求头信息">
         <el-table :data="updateapi.apiHead">
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
                                    <el-button v-if="scope.$index===(updateapi.apiHead.length-1)" size="mini" class="el-icon-plus" @click="addHead"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
      <el-form-item label="参数格式">
    <el-select v-model="updateapi.requestParameterType" placeholder="参数格式"  @change="paramsinit">
       <el-option
      v-for="item in requestParameterTypeList"
      :key="item[0]"
      :label="item[0]"
      :value="item[0]">
    </el-option>
    </el-select>
  </el-form-item>
       <el-form-item label="请求参数" v-if="this.updateapi.requestParameterType !== 'no-params'">
         <el-table :data="updateapi.ApiRequestParam" v-if="this.updateapi.requestParameterType === 'form-data'">
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
                                    <el-button v-if="scope.$index===(updateapi.ApiRequestParam.length-1)" size="mini" class="el-icon-plus" @click="addParam"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
         <el-input type="textarea" autosize v-model="updateapi.ApiRequestParam" v-else-if="this.updateapi.requestParameterType === 'raw'"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateApi">修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      updateapi: {
        projectCode: this.getapidetail(),
        apiname: '',
        apiCode: '',
        httpType: '',
        requestType: '',
        apiAddress: '',
        description: '',
        status: '',
        apiHead: [{name: '', value: ''}],
        requestParameterType: '',
        ApiRequestParam: [{name: '', value: ''}]
      },
      httpTypelist: this.getallType(),
      requestTypelist: [],
      requestParameterTypeList: []
    }
  },
  methods: {
    // 获取详情展示
    getapidetail () {
      this.$http.post('Api/GetApiDetail', {projectCode: this.$route.query.projectCode, apiCode: this.$route.query.apiCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.updateapi = response.data.data
          // 判断apiHead是否为空字符串,为空字符串需要处理下格式
          if (response.data.data.apiHead === '') { this.updateapi.apiHead = [{name: '', value: ''}] }
          // 判断params的数据格式,将接口返回的数据处理成对应的格式显示
          if (response.data.data.requestParameterType === 'raw') {
            if (response.data.data.ApiRequestParam === '') {
              this.updateapi.ApiRequestParam = ''
            } else {
              this.updateapi.ApiRequestParam = JSON.stringify(response.data.data.ApiRequestParam)
            }
          }
          if (response.data.data.requestParameterType === 'form-data') {
            if (response.data.data.ApiRequestParam === '') {
              this.updateapi.ApiRequestParam = [{name: '', value: ''}]
            } else {
              var apiParamarray = []
              for (var key in response.data.data.ApiRequestParam) {
                apiParamarray.push({name: key, value: response.data.data.ApiRequestParam[key]})
              }
              this.updateapi.ApiRequestParam = apiParamarray
            }
          }
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
        }
      })
    },
    updateApi () {
      var updateparam = {projectCode: this.updateapi.projectCode,
        apiname: this.updateapi.apiname,
        apiCode: this.updateapi.apiCode,
        httpType: this.updateapi.httpType,
        requestType: this.updateapi.requestType,
        apiAddress: this.updateapi.apiAddress,
        description: this.updateapi.description,
        status: this.updateapi.status,
        apiHead: '',
        requestParameterType: this.updateapi.requestParameterType,
        ApiRequestParam: ''}
      // 处理apihead数据格式--从数组转为字典
      var apiHeadnew = {}
      if ((this.updateapi.apiHead.length === 1) & (this.updateapi.apiHead[0].name === '') & (this.updateapi.apiHead[0].value === '')) {
        delete updateparam.apiHead
      } else {
        for (var i = 0, len = this.updateapi.apiHead.length; i < len; i++) {
          apiHeadnew[this.updateapi.apiHead[i]['name']] = this.updateapi.apiHead[i]['value']
        }
        updateparam['apiHead'] = apiHeadnew
      }
      // 处理apiparams的数据格式
      // form-data时处理数据方式
      var apiParamnew = {}
      if (this.updateapi.requestParameterType === 'form-data') {
        if ((this.updateapi.ApiRequestParam.length === 1) & (this.updateapi.ApiRequestParam[0].name === '') & (this.updateapi.ApiRequestParam[0].value === '')) {
          delete updateparam.ApiRequestParam
        } else {
          for (var j = 0, lens = this.updateapi.ApiRequestParam.length; j < lens; j++) {
            apiParamnew[this.updateapi.ApiRequestParam[j]['name']] = this.updateapi.ApiRequestParam[j]['value']
          }
          updateparam['ApiRequestParam'] = apiParamnew
        }
      }
      // no-params时处理数据方式
      if (this.updateapi.requestParameterType === 'no-params') {
        delete updateparam.ApiRequestParam
      }
      // raw时处理数据方式
      if (this.updateapi.requestParameterType === 'raw') {
        if (this.updateapi.ApiRequestParam === '') { delete updateparam.ApiRequestParam } else {
          apiParamnew = this.updateapi.ApiRequestParam
          updateparam['ApiRequestParam'] = apiParamnew
        }
      }

      this.$http.post('Api/UpdateApi', updateparam).then(response => {
        if (response.data.code !== '9999') {
          // 处理apihead的数据格式--从字典转为数组
          if (!updateparam.hasOwnProperty('apiHead')) {
            this.updateapi.apiHead = [{name: '', value: ''}]
          } else {
            var apiHeadarray = []
            for (var key in updateparam.apiHead) {
              apiHeadarray.push({name: key, value: updateparam.apiHead[key]})
            }
            this.updateapi.apiHead = apiHeadarray
          }
          // 处理apiparams的数据格式--从字典转为数组
          // form-data时处理数据方式
          if (this.updateapi.requestParameterType === 'form-data') {
            if (!updateparam.hasOwnProperty('ApiRequestParam')) {
              this.updateapi.ApiRequestParam = [{name: '', value: ''}]
            } else {
              var apiParamarray = []
              for (var key2 in updateparam.ApiRequestParam) {
                apiParamarray.push({name: key2, value: updateparam.ApiRequestParam[key2]})
              }
              this.updateapi.ApiRequestParam = apiParamarray
            }
          }
          // no-params时处理数据方式
          // if (this.updateapi.requestParameterType === 'no-params') {
          //   this.updateapi.ApiRequestParam = [{name: '', value: ''}]
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
      this.updateapi.apiHead.push(headers)
    },
    delHead (index) {
      this.updateapi.apiHead.splice(index, 1)
      if (this.updateapi.apiHead.length === 0) {
        this.updateapi.apiHead.push({name: '', value: ''})
      }
    },
    addParam () {
      let params = {name: '', value: ''}
      this.updateapi.ApiRequestParam.push(params)
    },
    delParam (index) {
      this.updateapi.ApiRequestParam.splice(index, 1)
      if (this.updateapi.ApiRequestParam.length === 0) {
        this.updateapi.ApiRequestParam.push({name: '', value: ''})
      }
    },
    // 下拉框切换时，重置请求参数
    paramsinit () {
      if (this.updateapi.requestParameterType === 'form-data') { this.updateapi.ApiRequestParam = [{name: '', value: ''}] }
      if (this.updateapi.requestParameterType === 'raw') { this.updateapi.ApiRequestParam = '' }
      if (this.updateapi.requestParameterType === 'no-params') { this.updateapi.ApiRequestParam = '' }
    }
  }
}
</script>

<style scoped>

</style>
