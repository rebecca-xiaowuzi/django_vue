<template>
    <el-form  :model="funcation">
        <el-form-item label="函数名称">
    <el-input  v-model="funcation.funcationname"></el-input>
  </el-form-item>
      <el-form-item label="前置需转换的数据">
         <el-table :data="funcation.requesttransfer">
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
                                    <el-button v-if="scope.$index===(funcation.requesttransfer.length-1)" size="mini" class="el-icon-plus" @click="addrequesttransfer"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
       <el-form-item label="转换参数名称">
   <el-input  v-model="funcation.responsetransfer"></el-input>
  </el-form-item>
      <el-form-item label="函数表达式">
   <el-input  v-model="funcation.funcation"></el-input>
  </el-form-item>

  <el-form-item><el-button type="primary" @click="runfuncation"  style="margin-left: 16px;">运行调试</el-button></el-form-item>
       <el-form-item label="函数结果">
   <el-input  disabled v-model="funcation.result"></el-input>
  </el-form-item>
          </el-form>
</template>

<script>
export default {
  data () {
    return {
      funcation: {
        responsetransfer: '',
        requesttransfer: [{name: '', value: ''}],
        funcation: '',
        result: '',
        funcationname: ''
      }

    }
  },
  methods: { addrequesttransfer () {
    let requesttransfer = {name: '', value: ''}
    this.funcation.requesttransfer.push(requesttransfer)
  },
  delrequesttransfer (index) {
    this.funcation.requesttransfer.splice(index, 1)
    if (this.funcation.requesttransfer.length === 0) {
      this.funcation.requesttransfer.push({name: '', value: ''})
    }
  },
  runfuncation () {
    var runfuncationparam = {
      responsetransfer: this.funcation.responsetransfer,
      funcation: this.funcation.funcation,
      requesttransfer: ''
    }
    // 处理requesttransfer数据格式--从数组转为字典
    var requesttransfernew = {}
    if ((this.funcation.requesttransfer.length === 1) & (this.funcation.requesttransfer[0].name === '') & (this.funcation.requesttransfer[0].value === '')) {
      delete runfuncationparam.requesttransfer
    } else {
      for (var i = 0, len = this.funcation.requesttransfer.length; i < len; i++) {
        requesttransfernew[this.funcation.requesttransfer[i]['name']] = this.funcation.requesttransfer[i]['value']
      }
      runfuncationparam['requesttransfer'] = requesttransfernew
    }
    this.$http.post('Funcation/runFuncation', runfuncationparam).then(response => {
      if (response.data.code !== '9999') {
        return this.$message.error({message: response.data.msg, center: true})
      } else {
        this.funcation.result = response.data.result
      }
    })
  }
  }

}
</script>

<style scoped>

</style>
