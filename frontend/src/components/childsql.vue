<template>
    <el-form  :model="sql">
      <el-form-item label="前置需转换的数据">
         <el-table :data="sql.requesttransfer">
<el-table-column prop="name" label="key" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.name" :value="scope.row.name" placeholder="请输入key"></el-input>
                                </template>
                            </el-table-column>
<el-table-column  prop="value" label="内容" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.value" :value="scope.row.value" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
           <el-table-column label="操作" min-width="10%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delrequesttransfer(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(sql.requesttransfer.length-1)" size="mini" class="el-icon-plus" @click="addrequesttransfer"></el-button>
                                </template>
                            </el-table-column>
         </el-table>
  </el-form-item>
       <el-form-item label="转换参数名称">
   <el-input  v-model="sql.responsetransfer"></el-input>
  </el-form-item>
      <el-form-item label="sql名称">
   <el-input  v-model="sql.sqlName"></el-input>
  </el-form-item>
      <el-form-item label="sql编号">
   <el-input  v-model="sql.sqlCode"></el-input>
  </el-form-item>
      <el-form-item label="sql">
   <el-input  v-model="sql.sql"></el-input>
  </el-form-item>
  <el-form-item><el-button type="primary" @click="runsql"  style="margin-left: 16px;">运行调试</el-button><el-button type="primary" @click="addsql"  style="margin-left: 16px;">添加sql</el-button></el-form-item>
       <el-form-item label="sql执行结果">
   <el-input  disabled v-model="sql.result"></el-input>
  </el-form-item>
          </el-form>
</template>

<script>
export default {
  name: 'child_sql'
}
</script>

<style scoped>

</style>
