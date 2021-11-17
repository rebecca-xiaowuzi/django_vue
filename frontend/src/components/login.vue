<template>
  <div>
    <el-form ref="loginformref" :model="loginform" label-width="80px">
  <el-form-item label="用户名">
    <el-input v-model="loginform.username"></el-input>
  </el-form-item>
      <el-form-item label="密码">
    <el-input v-model="loginform.password"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="login">登录</el-button>
    <el-button @click="resetloginform">重置</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
data(){
  loginform: {
      username: "",
      password: ""
  }
},
methods:{
  resetloginform(){
    this.$refs.loginformref.resetFields();
  },
  login(){
    this.$http.post("Login/login",this.loginform);
  }
}
}
</script>

<style scoped>

</style>
