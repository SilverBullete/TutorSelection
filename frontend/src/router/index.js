import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login'
import Student from '../views/Student'
import Teacher from '../views/Teacher'

// 登录界面
import loginForm from '../components/LoginForm'
import passwordForm from '../components/PasswordForm'

// student界面
import studentInfo from '../components/StudentInfo'
import studentResume from '../components/StudentResume'
import studentUTS from '../components/StudentUTS'
import studentUTSRes from '../components/StudentUTSRes'
import studentGDTS from '../components/StudentGDTS'
import studentGDTSRes from '../components/StudentGDTSRes'
import announcement from '../components/Announcement'

// teacher界面
import teacherUTS from '../components/TeacherUTS'
import teacherUTSRes from '../components/TeacherUTSRes'

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
        name: 's_info',
        component: studentInfo
      }, {
        path: 'resume',
        name: 's_resume',
        component: studentResume
      }, {
        path: 'select',
        name: 's_select',
        component: studentUTS
      }, {
        path: 'result',
        name: 's_result',
        component: studentUTSRes
      }, {
        path: 'gd_select',
        name: 's_gd_select',
        component: studentGDTS
      }, {
        path: 'gd_result',
        name: 's_gd_result',
        component: studentGDTSRes
      }, {
        path: 'announcement',
        name: 's_announcement',
        component: announcement
      }
    ]
  },
  {
    path: '/teacher/',
    name: 'teacher',
    component: Teacher,
    children: [
      {
        path: 'info',
        name: 't_info',
        component: studentInfo
      }, {
        path: 'resume',
        name: 't_resume',
        component: studentResume
      }, {
        path: 'select',
        name: 't_select',
        component: teacherUTS
      }, {
        path: 'result',
        name: 't_result',
        component: teacherUTSRes
      }, {
        path: 'announcement',
        name: 't_announcement',
        component: announcement
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
