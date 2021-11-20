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
     <el-tabs type="card" editable>
  <el-tab-pane
    :key="item.environmentName"
    v-for="item in editableTabs"
    :label="item.environmentName"
    :name="item.environmentName">
  <template>
    {{item.environmentName}}
  <div>
    <el-form :model="updateenvironment">
      <el-form-item label="环境名称">
    <el-input v-model="updateenvironment.environmentName"  :placeholder="item.environmentName"></el-input>
  </el-form-item>
       <el-form-item label="环境描述">
    <el-input  v-model="updateenvironment.environmentDescription" :placeholder="item.environmentDescription"></el-input>
  </el-form-item>
       <el-form-item label="ip">
<el-input  v-model="updateenvironment.ip" :placeholder="item.ip"></el-input>
  </el-form-item>
      <el-form-item>
    <el-button type="primary" @click="updateenvironment" >修改</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
      </el-form>
  </div>
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
        users: this.$route.query.users
      },
      editableTabs: this.$route.query.environments,
      updateenvironment: {
        projectCode: this.$route.query.projectCode,
        environmentName: '',
        environmentDescription: '',
        ip: ''

      }
    }
  }
}
</script>

<style scoped>

</style>
