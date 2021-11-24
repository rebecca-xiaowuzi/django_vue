 <template><el-container>
  <el-aside width="200px">

   <div>
    <el-form  :model="projectdetail">
  <el-form-item label="项目编号">
    <el-input v-model="projectdetail.projectCode" disabled></el-input>
  </el-form-item>
      <el-form-item label="项目名称">
    <el-input  v-model="projectdetail.projectName" disabled></el-input>
  </el-form-item>
       <el-form-item label="项目描述">
    <el-input  v-model="projectdetail.projectDescription" disabled></el-input>
        </el-form-item>
         <el-form-item label="项目用户">
    <el-input  v-model="projectdetail.users" disabled></el-input>
  </el-form-item>
      </el-form>
  </div>
  </el-aside>
  <el-main>
     <el-tabs v-model="activeName" type="border-card" @tab-click="getenvironmentDetail">
  <el-tab-pane
    :key="item.environmentName"
    v-for="item in editableTabs"
    :name="item.environmentName"
  >
    <span slot="label">{{item.environmentName}}</span>
    <div>
      <el-form :model="updateenvironment">
      <el-form-item label="环境名称">
    <el-input v-model="updateenvironment.environmentName" disabled></el-input>
  </el-form-item>
       <el-form-item label="环境描述">
    <el-input  v-model="updateenvironment.environmentDescription" ></el-input>
  </el-form-item>
       <el-form-item label="ip">
<el-input  v-model="updateenvironment.ip"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateEnvironment" >修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
    </div>
  <template>
</template>
  </el-tab-pane>
</el-tabs>
  </el-main>
</el-container>
 </template>
<script>

export default {
  data () {
    return {
      projectdetail: {
        projectCode: this.$route.query.projectCode,
        projectName: this.$route.query.projectName,
        projectDescription: this.$route.query.projectDescription,
        users: this.$route.query.users.toString()
      },
      updateenvironment: {
        environmentName: '',
        environmentDescription: '',
        ip: ''
      },
      editableTabs: this.$route.query.environments,
      activeName: ''
    }
  },
  methods: {
    updateEnvironment () {
      this.$http.post('Environment/updateEnvironment', {ip: this.updateenvironment.ip, environmentDescription: this.updateenvironment.environmentDescription, environmentName: this.updateenvironment.environmentName, projectCode: this.projectdetail.projectCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.$message.success({message: '修改环境信息成功', center: true})
          this.$router.push('/projectlist')
        }
      })
    },
    cancel () {
      this.$router.push('/projectlist')
    },
    getenvironmentDetail () {
      this.$http.post('Environment/getEnvironmentDetail', {environmentName: this.activeName, projectCode: this.projectdetail.projectCode}).then(response => {
        if (response.data.code !== '9999') {
          return this.$message.error({message: response.data.msg, center: true})
        } else {
          this.updateenvironment.environmentName = response.data.data.environmentName
          this.updateenvironment.environmentDescription = response.data.data.environmentDescription
          this.updateenvironment.ip = response.data.data.ip
        }
      })
    }
  }

}
</script>

<style scoped>

</style>
