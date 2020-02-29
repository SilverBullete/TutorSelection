<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>个人信息</el-breadcrumb-item>
        <el-breadcrumb-item>个人基本信息</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        个人基本信息
      </div>
    </div>
    
    <div class="content">
      <el-tabs
        tab-position="left"
      >
        <el-tab-pane label="信息管理">
          <div class="">
            <el-row :gutter="24">
              <el-col :span="16">
                <el-form
                  :model="student"
                  label-width="80px"
                >
                  <el-form-item label="姓名">
                    <el-input
                      v-model="student.name"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="学号">
                    <el-input
                      v-model="student.id"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="性别">
                    <el-input
                      v-model="student.gender"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="年级">
                    <el-input
                      v-model="student.grade"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="学院">
                    <el-input
                      v-model="student.college"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="专业">
                    <el-input
                      v-model="student.subject"
                      :disabled="true"
                    />
                  </el-form-item>
                  <el-form-item label="班级">
                    <el-input
                      v-model="student.class_name"
                      :disabled="true"
                    />
                  </el-form-item>
                  <!-- <el-form-item label="年级">
            <el-input v-model="student.grade" />
          </el-form-item> -->
                </el-form>
              </el-col>
              <el-col :span="8">
                <el-image :src="src">
                  <div
                    slot="placeholder"
                    class="image-slot"
                  >
                    加载中<span class="dot">...</span>
                  </div>
                  <div
                    slot="error"
                    class="image-slot"
                  >
                    <i class="el-icon-picture-outline" />
                  </div>
                </el-image>
                <el-button
                  type="primary"
                  class="btn"
                >
                  提交
                </el-button>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="密码管理">
          <el-row :gutter="20">
            <el-col :span="16">
              <el-form
                ref="passFormRef"
                :model="passForm"
                status-icon
                :rules="rules"
                label-width="100px"
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
            </el-col>
            <el-col :span="8" />
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
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
      src: 'https://p1.ssl.qhimg.com/t019472bb28fbb2989f.png',
      student: {},
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
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        this.$http.post('get_info', { token: token }).then(function (res) {
          _this.student = res.data.data
          _this.src = res.data.data.avatar
        })
        this.loading = false
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
.container{
  height: 100%;
  padding: 0 0 6px 0;
  width: 100%;
  .header{
    margin: 0 -24px;
    padding: 12px 24px 16px 24px;
    background-color: #ffffff;
    > .header-heading{
      margin-top: 8px;
      display: flex;
      justify-content: flex-start;
      font-weight: 600;
      font-size: 20px;
      line-height: 32px;
    }
  }
}
.content{
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  margin-top: 24px;
  padding: 24px 0;
}
.el-form-item{
  width: 80%;
  // margin-left: 15%;
}
.el-tabs{
  height: 450px;
  min-height: 200px;
  max-height: 450px;
}
div.el-tabs__item{
  width: 224px!important;
  
}
.el-tabs__item.is-active{
  background-color: #e6f7ff;
}
.el-tabs__active-bar.is-left{
  width: 3px;
}
.el-image{
  width: 200px;
}
.btn{
  position: absolute;
  bottom: 0;
  right: 48px;
}
</style>
