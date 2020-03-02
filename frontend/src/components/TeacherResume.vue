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
          <div class="pdf">
            我的简历: <el-link
              :href="resume"
              target="_blank"
            >
              查看<i class="el-icon-view el-icon--right" />
            </el-link>
          </div>
          
          <el-upload
            class="upload-demo"
            drag
            action="http://localhost:8001/api/teacher/upload_resume"
            :before-upload="beforePDFUpload"
            :on-success="handleSuccess"
            :data="{token: token}"
            accept="pdf"
            :limit="1"
          >
            <i class="el-icon-upload" />
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div
              slot="tip"
              class="el-upload__tip"
            >
              只能上传pdf文件
            </div>
          </el-upload>
        </el-col>
        <el-col :span="8" />
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      resume: '',
      token: '',
      id: ''
    }
  },
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        _this.token = token
        this.$http.post('get_resume', { token: token }).then(function (res) {
          _this.resume = res.data.data.profile
          _this.id = res.data.data.id
        })
        this.loading = false
      },
  methods: {
      beforePDFUpload (file) {
        const isPDF = file.type === 'application/pdf'
        if (!isPDF) {
          this.$message.error('上传信息只能为pdf格式!')
        }
      },
      handleSuccess (files) {
        this.resume = 'http://127.0.0.1:8001/media/resume/' + this.id + '.pdf'
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
.pdf{
    text-align: left;
    font-size: 17px;
    padding-left: 24px;
    padding-bottom: 24px;
    > .el-link{
        font-size: 17px;
    }
}
</style>
