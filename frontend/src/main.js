import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'
// 导入图标库
import './assets/fonts/iconfont.css'
import axios from 'axios'
// 配置请求根路径
axios.defaults.baseURL = 'http://127.0.0.1:8001/api/'
Vue.prototype.$http = axios
axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed'
Vue.config.productionTip = false
Vue.prototype.isInArray = function (arr, value) {
    for (var i = 0; i < arr.length; i++) {
        if (value === arr[i]) {
            return true
        }
    }
    return false
}
Vue.prototype.get_user_type = async function () {
    const token = window.sessionStorage.getItem('token')
    const { data: res } = await this.$http.post('get_user_type', { token: token })
    return res.data.type
}

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
