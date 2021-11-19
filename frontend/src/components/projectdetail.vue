 <template><el-container>
  <el-aside width="200px">

   <div>
    <el-form  :model="projectdetail">
  <el-form-item label="项目编号">
    <el-input v-model="projectdetail.projectCode"></el-input>
  </el-form-item>
      <el-form-item label="项目名称">
    <el-input  v-model="projectdetail.projectName"></el-input>
  </el-form-item>
       <el-form-item label="项目描述">
    <el-input  v-model="projectdetail.projectDescription"></el-input>
        </el-form-item>
         <el-form-item label="项目用户">
    <el-input  v-model="projectdetail.users"></el-input>
  </el-form-item>
      </el-form>
  </div>
  </el-aside>
  <el-main>
   <div>
  </div>
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
        users: this.$route.query.users,
        // environments: this.$route.query.environments
        environments: [{'ip': 'https://xagent-new-fat.vocustcloud.com',
          'environmentName': '1115555111'}, {'ip': 'https://xagud.com',
          'environmentName': '11155xxx55111'}]
      }
    }
  }
}
</script>

<style scoped>

</style>
