<template>
  <div>
    <el-form  :model="adduser">
  <el-form-item label="电话">
    <el-input v-model="adduser.phone"></el-input>
  </el-form-item>
      <el-form-item label="密码">
    <el-input  v-model="adduser.password"></el-input>
  </el-form-item>
       <el-form-item label="邮箱">
    <el-input  v-model="adduser.email"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addUser">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      adduser: {
        phone: '',
        password: '',
        email: ''
      }
    }
  },
  methods: {
    addUser () {
      this.$http.post('User/addUser', this.adduser).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/userlist') }
      })
    },
    cancel () {
      this.$router.push('/userlist')
    }
  }
}
</script>

<style scoped>

</style>
