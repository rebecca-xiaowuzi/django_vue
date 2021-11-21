import Vue from 'vue'
import Router from 'vue-router'
import login from '../components/login.vue'
import home from '../components/home'
import userlist from '../components/userlist'
import adduser from '../components/adduser'
import updateuser from '../components/updateuser'
import projectlist from '../components/projectlist'
import addproject from '../components/addproject'
import updateproject from '../components/updateproject'
import addenvironment from '../components/addenvironment'
import projectdetail from '../components/projectdetail'
import variablelist from '../components/variablelist'
import addvariable from '../components/addvariable'
import testcaselist from '../components/testcaselist'
import apilist from '../components/apilist'
import addapi from '../components/addapi'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/login',
      component: login
    },
    { path: '/',
      redirect: '/login'},

    {
      path: '/home',
      name: 'home',
      component: home,
      children: [
        {
          path: '/userlist',
          name: 'userlist',
          component: userlist
        },
        {
          path: '/adduser',
          component: adduser
        },
        {
          path: '/updateuser',
          component: updateuser
        },
        {
          path: '/projectlist',
          name: 'projectlist',
          component: projectlist
        },
        {
          path: '/addproject',
          component: addproject
        },
        {
          path: '/updateproject',
          component: updateproject
        },
        {
          path: '/addenvironment',
          component: addenvironment
        },
        {
          path: '/projectdetail',
          component: projectdetail
        },
        {
          path: '/variablelist',
          name: 'variablelist',
          component: variablelist
        },
        {
          path: '/addvariable',
          component: addvariable
        },
        {
          path: '/testcaselist',
          name: 'testcaselist',
          component: testcaselist
        },
        {
          path: '/apilist',
          name: 'apilist',
          component: apilist
        },
        {
          path: '/addapi',
          component: addapi
        }
      ]}

  ]

})
