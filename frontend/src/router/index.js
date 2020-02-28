import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Student from '../views/Student.vue'

// 登录界面
import loginForm from '../components/LoginForm'
import passwordForm from '../components/PasswordForm'

// student界面
import studentInfo from '../components/StudentInfo'
import studentResume from '../components/StudentResume'
import studentUTS from '../components/StudentUTS'
import studentUTSRes from '../components/StudentUTSRes'
import announcement from '../components/Announcement'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'main',
    redirect: 'login',
    component: Login,
    children: [
      {
        path: 'login',
        name: 'login',
        component: loginForm
      }, {
        path: 'password',
        name: 'password',
        component: passwordForm
      }
    ]
  },
  
  {
    path: '/student/',
    name: 'student',
    component: Student,
    children: [
      {
        path: 'info',
        name: 'info',
        component: studentInfo
      }, {
        path: 'resume',
        name: 'resume',
        component: studentResume
      }, {
        path: 'select',
        name: 'select',
        component: studentUTS
      }, {
        path: 'result',
        name: 'result',
        component: studentUTSRes
      }, {
        path: 'announcement',
        name: 'announcement',
        component: announcement
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
