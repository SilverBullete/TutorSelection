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
                    <el-input v-model="student.name" />
                  </el-form-item>
                  <el-form-item label="学号">
                    <el-input v-model="student.id" />
                  </el-form-item>
                  <el-form-item label="性别">
                    <el-input v-model="student.gender" />
                  </el-form-item>
                  <el-form-item label="年级">
                    <el-input v-model="student.grade" />
                  </el-form-item>
                  <el-form-item label="学院">
                    <el-input v-model="student.college" />
                  </el-form-item>
                  <el-form-item label="专业">
                    <el-input v-model="student.subject" />
                  </el-form-item>
                  <el-form-item label="班级">
                    <el-input v-model="student.class_name" />
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
                ref="ruleForm"
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
                    @click="submitForm('ruleForm')"
                  >
                    提交
                  </el-button>
                  <el-button @click="resetForm('ruleForm')">
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
    return {
      src: 'https://p1.ssl.qhimg.com/t019472bb28fbb2989f.png',
      student: {
        name: '',
        id: '',
        gender: '',
        college: '',
        subject: '',
        class_name: ''
        
      },
      passForm: {
        oldPass: '',
        pass: '',
        checkPass: ''
      }
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
