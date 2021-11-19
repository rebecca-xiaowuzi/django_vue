<template>
  <div>
    <el-form  :model="updateuser">
  <el-form-item label="电话">
    <el-input v-model="updateuser.phone"></el-input>
  </el-form-item>
       <el-form-item label="邮箱">
    <el-input  v-model="updateuser.email"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateUser">修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item >
      </el-form>

  </div>
</template>

<script>
export default {
  data () {
    return {
      updateuser: {
        phone: this.$route.query.phone,
        email: this.$route.query.email
      }
    }
  },
  methods: {
    updateUser () {
      this.$http.post('User/updateUser', this.updateuser).then(response => {
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
