<template>
  <div class="login_container">
    <div class="login_box">
      <div class="login_header">
        请先修改默认密码
      </div>
      <el-form
        ref="passFormRef"
        :model="passForm"
        status-icon
        :rules="rules"
        label-width="80px"
      >
        <el-form-item
          label="旧密码"
          prop="oldPass"
        >
          <el-input
            v-model="passForm.oldPass"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item
          label="密码"
          prop="pass"
        >
          <el-input
            v-model="passForm.pass"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item
          label="确认密码"
          prop="checkPass"
        >
          <el-input
            v-model="passForm.checkPass"
            type="password"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="submitForm"
          >
            提交
          </el-button>
          <el-button @click="resetForm">
            重置
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
      var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      }
      callback()
    }
    var validatePass1 = (rule, value, callback) => {
      const reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[0-9A-Za-z!@*$-_()+=&]{8,15}$/
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (value.length < 8 || value.length > 15) {
          callback(new Error('密码长度在8到15个字符之间'))
        } else if (!reg.test(value)) {
          callback(new Error('密码必须包含数字和字母，且只能包含以下特殊字符：!@*$-_()+=&'))
        } else if (this.passForm.checkPass !== '') {
          this.$refs.passFormRef.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.passForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      passForm: {
        oldPass: '',
        pass: '',
        checkPass: ''
      },
      rules: {
        oldPass: [
          { validator: validatePass, trigger: 'blur' }
        ],
        pass: [
          { validator: validatePass1, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm () {
      this.$refs.passFormRef.validate(async valid => {
        if (!valid) return
        const token = window.sessionStorage.getItem('token')
        const { data: res } = await this.$http.post('update_password', { token: token, oldPass: this.passForm.oldPass, pass: this.passForm.pass })
        if (res.code !== 200) return this.$message.error(res.message)
        else {
          if (res.data.result) {
            this.$message({
              message: res.data.message,
              type: 'success'
            })
            if (res.data.type === 'student') return this.$router.push('/student')
          } else {
            this.$message.error(res.data.message)
          }
          this.resetForm()
        }
      })
    },
    resetForm () {
      this.$refs.passFormRef.resetFields()
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
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
  }
  .login_header {
    margin-top: 20px;
  }
  .el-form{
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
}
</style>
