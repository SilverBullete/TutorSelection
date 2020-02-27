import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Student from '../views/Student.vue'

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
    redirect: 'login'
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/student/',
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
