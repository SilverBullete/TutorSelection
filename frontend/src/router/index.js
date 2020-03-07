import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login'
import Student from '../views/Student'
import Teacher from '../views/Teacher'
import Admin from '../views/Admin'

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
import teacherInfo from '../components/TeacherInfo'
import teacherResume from '../components/TeacherResume'
import teacherUTS from '../components/TeacherUTS'
import teacherUTSRes from '../components/TeacherUTSRes'

// admin界面
import sInfoManage from '../components/SInfoManage'
import tInfoManage from '../components/TInfoManage'
import roundOpen from '../components/RoundOpen'
import roundRes from '../components/RoundRes'
import adminDistribution from '../components/AdminDistribution'
import teacherConfirmRes from '../components/TeacherConfirmRes'
import announcementPublic from '../components/AnnouncementPublic'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
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
          name: 'SInfo',
          component: studentInfo
        }, {
          path: 'resume',
          name: 'SResume',
          component: studentResume
        }, {
          path: 'select',
          name: 'SSelect',
          component: studentUTS
        }, {
          path: 'result',
          name: 'SResult',
          component: studentUTSRes
        }, {
          path: 'gd_select',
          name: 'SGDSelect',
          component: studentGDTS
        }, {
          path: 'gd_result',
          name: 'SGDResult',
          component: studentGDTSRes
        }, {
          path: 'announcement',
          name: 'SAnnouncement',
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
          name: 'TInfo',
          component: teacherInfo
        }, {
          path: 'resume',
          name: 'TResume',
          component: teacherResume
        }, {
          path: 'select',
          name: 'TSelect',
          component: teacherUTS
        }, {
          path: 'result',
          name: 'TResult',
          component: teacherUTSRes
        }, {
          path: 'announcement',
          name: 'TAnnouncement',
          component: announcement
        }
      ]
    },
    {
      path: '/admin/',
      name: 'admin',
      component: Admin,
      children: [
        {
          path: 'student_info_manage',
          name: 'SInfoManage',
          component: sInfoManage
        }, {
          path: 'teacher_info_manage',
          name: 'TInfoManage',
          component: tInfoManage
        }, {
          path: 'round_open',
          name: 'RoundOpen',
          component: roundOpen
        }, {
          path: 'round_res',
          name: 'RoundRes',
          component: roundRes
        }, {
          path: 'admin_distribution',
          name: 'AdminDistribution',
          component: adminDistribution
        }, {
          path: 'teacher_confirm_res',
          name: 'TeacherConfirmRes',
          component: teacherConfirmRes
        }, {
          path: 'announcement_public',
          name: 'AnnouncementPublic',
          component: announcementPublic
        }, {
          path: 'announcement',
          name: 'AAnnouncement',
          component: announcement
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
    if (to.path === '/login') return next()
    const token = window.sessionStorage.getItem('token')
    if (!token) return next('/login')
    next()
})

export default router
