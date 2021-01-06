<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>个人信息</el-breadcrumb-item>
        <el-breadcrumb-item>个人简历</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        个人简历
      </div>
    </div>
    
    <div class="content">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-form
            ref="resumeFormRef" 
            :model="student"
            :rules="resumeFormRules"
            label-width="120px"
          >
            <el-form-item
              label="是否接受分配"
              class="switch"
            >
              <el-switch
                v-model="student.agreeDistribution"
              />
            </el-form-item>
            <el-form-item 
              label="绩点"
              prop="gpa"
            >
              <el-input
                v-model="student.gpa"
                type="text"
              />
            </el-form-item>
            <el-form-item
              label="绩点排名"
            >
              <el-input
                v-model="student.rank"
                type="text"
              />
            </el-form-item>
            <el-form-item label="个人简介">
              <el-input
                v-model="student.profile"
                type="textarea"
                :rows="6"
              />
            </el-form-item>
            <el-form-item label="获奖情况">
              <el-input
                v-model="student.award"
                type="textarea"
                :rows="6"
              />
            </el-form-item>
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
            @click="submit"
          >
            提交
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    var validateGPA = (rule, value, callback) => {
      const re = /^\d+(\.\d+)?$/
      const re2 = /^\d+$/
      if (re.exec(value) == null && re2.exec(value) == null) {
        callback(new Error('绩点必须为非负小数或非负整数')) 
      } else if (Number(value) > 5) {
        callback(new Error('绩点必须小于等于5'))
      }
        callback()
      }
    return {
      src: '',
      student: {},
      resumeFormRules: {
        gpa: [
          { validator: validateGPA, trigger: 'blur' }
        ]
      }
    }
  },
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        this.$http.post('get_resume', { token: token }).then(function (res) {
          _this.student = res.data.data
          _this.src = res.data.data.avatar
        })
        this.loading = false
      },
  methods: {
    submit () {
      this.$refs.resumeFormRef.validate(async valid => {
        if (!valid) return
        const token = window.sessionStorage.getItem('token')
        const { data: res } = await this.$http.post('student/update_resume', { token: token, form: this.student })
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
        }
      })
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

.el-image{
  width: 200px;
}
.btn{
  position: absolute;
  bottom: 0;
  right: 48px;
}
</style>
<style lang="less">
.switch{
  > .el-form-item__content{
    left: 20px;
    text-align: left;
  }
}
</style>
