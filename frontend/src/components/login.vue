<template>
  <div>
    <el-form ref="loginformref" :model="loginform">
  <el-form-item label="用户名">
    <el-input v-model="loginform.phone"></el-input>
  </el-form-item>
      <el-form-item label="密码">
    <el-input  v-model="loginform.password"></el-input>
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
  data () {
    return {
      loginform: {
        phone: '18334705319',
        password: '111111'
      }
    }
  },
  methods: {
    resetloginform () {
      this.$refs.loginformref.resetFields()
    },
    login () {
      this.$http.post('Login/login', this.loginform).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/home') }
      })
    }
  }
}
</script>

<style scoped>

</style>
