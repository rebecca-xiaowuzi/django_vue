<template>
  <div>
    <el-form  :model="updateproject">
  <el-form-item label="项目编号">
    <el-input v-model="updateproject.projectCode" disabled></el-input>
  </el-form-item>
      <el-form-item label="项目名称">
    <el-input  v-model="updateproject.projectName"></el-input>
  </el-form-item>
       <el-form-item label="项目描述">
    <el-input  v-model="updateproject.projectDescription"></el-input>
  </el-form-item>
       <el-form-item label="项目用户">
    <el-select v-model="updateproject.users" multiple placeholder="请选择">
    <el-option
      v-for="item in options"
      :key="item.phone"
      :label="item.phone"
      :value="item.phone">
    </el-option>
  </el-select>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateProject">修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>
<script>
export default {
  data () {
    return {
      updateproject: {
        projectCode: this.$route.query.projectCode,
        projectName: this.$route.query.projectName,
        projectDescription: this.$route.query.projectDescription,
        users: this.$route.query.users
      },
      options: this.userlist()
    }
  },
  methods: {
    updateProject () {
      this.$http.post('Project/updateProject', this.updateproject).then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.$router.push('/projectlist') }
      })
    },
    cancel () {
      this.$router.push('/projectlist')
    },
    userlist () {
      this.$http.get('User/getUsers').then(response => {
        if (response.data.code !== '9999') { return this.$message.error({message: response.data.msg, center: true}) } else { this.options = response.data.data }
      })
    }
  }
}
</script>

<style scoped>

</style>
