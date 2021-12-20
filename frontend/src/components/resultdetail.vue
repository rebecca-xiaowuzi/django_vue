<template>
  <div>
    <el-form  :model="resultdetail">
      <el-form-item label="请求">
    <el-input v-model="resultdetail.request" disabled>
    </el-input>
  </el-form-item>
       <el-form-item label="结果详情">
    <el-input  v-model="resultdetail.result_detail" disabled type="textarea" autosize></el-input>
  </el-form-item>
      </el-form>
  </div>
</template>
<script>
export default {
  data () {
    return {
      resultdetail: {
        request: '',
        result_detail: '',
      }
    }
  },
   created(){
      this.getResultDetail()
    },
  methods: {
    getResultDetail () {
      this.$http.post('Result/GetResultDetail', {id: this.$route.query.id}).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.resultdetail = response.data.data }
      })
    }
  }
}
</script>

<style scoped>

</style>
