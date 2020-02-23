<template>
  <div class="login_container">
    <div class="login_box">
      <div class="login_header">
        用户登录
      </div>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginFormRules"
        class="login_form"
      >
        <div class="type_box">
          <el-radio-group
            v-model="loginForm.type"
            size="mini"
          >
            <el-radio-button label="学生" />
            <el-radio-button label="教师" />
            <el-radio-button label="管理员" />
          </el-radio-group>
        </div>
        <el-form-item prop="id">
          <el-input
            v-model="loginForm.id"
            prefix-icon="iconfont icon-user"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            prefix-icon="iconfont icon-password"
            type="password"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            class="btn"
            @click="login"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data () {
    return {
      loginForm: {
        type: '学生',
        id: '201700000000',
        password: '123456'
      },
      loginFormRules: {
        id: [
            { required: true, message: '请输入学号或工号', trigger: 'blur' }
          ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 15, message: '密码长度在6到15个字符之间', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    login () {
      this.$refs.loginFormRef.validate(async valid => {
        if (!valid) return
        this.$http.get('create')
        const { data: res } = await this.$http.post('login', this.loginForm)
        if (res.code !== 200) return this.$message.error(res.message)
        window.sessionStorage.setItem('token', res.data.token)
        // this.$router.push('/home')
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login_container {
  height: 100%;
  background-color: #ffffff;
  .login_box {
    width: 450px;
    height: 300px;
    background-color: #EEEEEE;
    border-radius: 5px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -210px);

  }
  .login_header {
    margin-top: 20px;
  }
  .login_form{
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
    .type_box{
      padding: 15px 20px;
    }
    .btn{
      width: 100%;
      height: 40px;
      padding: 0 20px;
      box-sizing: border-box;
    }
  }
}
</style>
