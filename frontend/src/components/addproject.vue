<template>
  <div>
    <el-form  :model="addproject">
  <el-form-item label="项目编号">
    <el-input v-model="addproject.projectCode"></el-input>
  </el-form-item>
      <el-form-item label="项目名称">
    <el-input  v-model="addproject.projectName"></el-input>
  </el-form-item>
       <el-form-item label="项目描述">
    <el-input  v-model="addproject.projectDescription"></el-input>
  </el-form-item>
       <el-form-item label="项目用户">
    <el-select v-model="addproject.users" multiple placeholder="请选择">
    <el-option
      v-for="item in options"
      :key="item.phone"
      :label="item.phone"
      :value="item.phone">
    </el-option>
  </el-select>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="addProject">新增</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      addproject: {
        projectCode: '',
        projectName: '',
        projectDescription: '',
        users: []
      },
      options: this.userlist()
    }
  },
  methods: {
    addProject () {
      this.$http.post('Project/addProject', this.addproject).then(response => {
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
