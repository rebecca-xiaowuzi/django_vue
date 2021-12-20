<template>
    <el-container>
        <!--顶部-->
        <el-header style="border-bottom: 1px solid gray;">
            <el-row style="margin: 10px 15px">
                <el-col :span="1">
                    <!--收缩条-->
                    <a href="#" @click="changeCollapse" style="font-size: 25px;color:#909399;"><i
                            :class="collpaseIcon"></i></a>
                </el-col>
            </el-row>
        </el-header>
        <!--中央区域-->
        <el-main>
            <el-container>
                <!--左侧导航栏-->
                <el-aside :style="{width:collpaseWidth}">
                    <!--default-active代表导航栏默认选中哪个index, :collapse决定导航栏是否展开，为boolean类型
                    :router决定导航栏是否开启路由模式，即在菜单item上设置路由是否生效，值为boolean类型-->
                    <el-menu
                            default-active="0"
                            class="el-menu-vertical-demo"
                            :collapse="isCollapse"
                            :router="true"
                    >
                        <!--index设置当前item的下标，:route则是传一个对象进行，指定路由-->
                        <el-submenu index="1">

                            <template slot="title">
                                <i class="fa fa-cogs"></i><span> 用户管理</span>
                            </template>
                            <el-menu-item index="/userlist" :route="{name:'userlist'}" > 用户列表
                            </el-menu-item>
                        </el-submenu>

                        <el-submenu index="2">
                            <template slot="title">
                                <i class="fa fa-users"></i>
                                <span> 项目管理</span>
                            </template>
                            <el-menu-item index="/projectlist" :route="{name:'projectlist'}">
                                项目列表
                            </el-menu-item>
                          <el-menu-item index="/variablelist" :route="{name:'variablelist'}">
                                变量信息
                            </el-menu-item>
                          <el-menu-item index="/SqlConnectlist" :route="{name:'SqlConnectlist'}">
                                数据库连接信息
                            </el-menu-item>
                          <el-menu-item index="/sqllist" :route="{name:'sqllist'}">
                                sql列表
                            </el-menu-item>
                        </el-submenu>
                      <el-submenu index="3">
                            <template slot="title">
                                <i class="fa fa-users"></i>
                                <span> 接口管理</span>
                            </template>
                            <el-menu-item index="/apilist" :route="{name:'apilist'}">
                                接口列表
                            </el-menu-item>
                        </el-submenu>
                      <el-submenu index="4">
                            <template slot="title">
                                <i class="fa fa-users"></i>
                                <span> 用例管理</span>
                            </template>
                            <el-menu-item index="/testcaselist" :route="{name:'testcaselist'}">
                                用例列表
                            </el-menu-item>
                          <el-menu-item index="/testcasesetlist" :route="{name:'testcasesetlist'}">
                                用例集列表
                            </el-menu-item>
                         <el-menu-item index="/resultlist" :route="{name:'resultlist'}">
                                结果列表
                            </el-menu-item>
                        </el-submenu>

                    </el-menu>

                </el-aside>
                <!--主内容显示区域-->
                <el-main>
                    <!--路由渲染-->
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-main>
        <!--底部-->
        <el-footer style="border-top: 1px solid gray"></el-footer>
    </el-container>
</template>

<script>
// 这一大段JS就是为了做收缩/展开导航栏而用的！
export default {
  name: 'Main',
  data: function () {
    return {
      isCollapse: false // 决定左侧导航栏是否展开
    }
  },
  computed: {
    collpaseIcon: function () { // 左侧导航栏是否展开状态的图标
      // 如果是展开状态就图标向右，否则图标向左
      return this.isCollapse ? 'el-icon-s-fold' : 'el-icon-s-unfold'
    },
    collpaseWidth: function () { // 左侧导航栏是否展开状态的宽度
      // 如果是展开状态就导航栏宽度为65px，否则200px
      return this.isCollapse ? '65px' : '200px'
    }
  },
  methods: {
    changeCollapse: function () { // 更改左侧导航栏展示状态
      this.isCollapse = !this.isCollapse
    }
  }
}
</script>

<style scoped>
    /*整体显示区域布局样式*/
    .el-container {
        height: 100%;
    }

    .el-header, .el-main {
        padding: 0;
    }

    /*左边导航栏具体样式*/
    .el-menu-vertical-demo.el-menu {
        padding-left: 20px;
        text-align: left;
        height: 100%;
        padding: 0;
    }

    el-container > .el-menu-vertical-demo.el-menu {
        padding: 0;
    }

    .el-submenu .el-menu-item, .el-menu-item {
        min-width: 50px;
    }

    .el-menu-item {
        padding: 0;
    }
</style>
