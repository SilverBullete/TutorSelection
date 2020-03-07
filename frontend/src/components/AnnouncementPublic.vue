<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>公告发布</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        公告发布
      </div>
    </div>
    <div class="content">
      <el-form
        ref="form"
        :model="form"
        label-width="120px"
      >
        <el-form-item label="公告类别">
          <el-select
            v-model="form.type"
            placeholder="请选择公告类别"
            style="width:400px"
          >
            <el-option
              label="开放公告"
              value="0"
            />
            <el-option
              label="公示公告"
              value="1"
            />
            <el-option
              label="普通公告"
              value="2"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="公告标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item
          v-if="form.type==='0'"
          label="学生选择时间"
        >
          <el-date-picker
            v-model="form.date"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
            value-format="yyyy-MM-dd HH:mm:ss"
            :readonly="true"
          />
        </el-form-item>
        <el-form-item
          v-else-if="form.type==='1'"
          label="公示时间"
        >
          <el-date-picker
            v-model="form.date"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="公告内容">
          <el-input
            v-model="form.content"
            type="textarea"
            rows="5"
            maxlength="450"
            show-word-limit
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="submit"
          >
            立即发布
          </el-button>
          <el-button
            @click="preview"
          >
            预览
          </el-button>
        </el-form-item>
      </el-form>
      <el-dialog
        :title="form.title"
        :visible.sync="dialogVisible"
      >
        <div class="dialog-content">
          <div
            style="text-indent:2em;"
            v-html="content"
          />
          <div class="dialog-date">
            <div v-if="form.type==='0'">
              学生选择开放时间: {{ form.date[0] }} - {{ form.date[1] }}
            </div>
            <div v-if="form.type==='1'">
              公示时间: {{ form.date }}
            </div>
          </div>
        </div>
        <div
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="dialogVisible = false">
            取 消
          </el-button>
          <el-button
            type="primary"
            @click="dialogVisible = false"
          >
            确 定
          </el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
        form: {
          title: '',
          type: '0',
          date: '',
          content: ''
        },
        dialogVisible: false,
        content: ''
      }
  },
  async created () {
        this.loading = true
        const token = window.sessionStorage.getItem('token')
        const res = await this.$http.post('get_round_time', { token: token })
        if (res.data.code !== 200) {
          this.$message.error(res.data.message)
        } else {
          this.form.date = res.data.data.date
        }
        this.loading = false
      },
 methods: {
      preview () {
        const arr = []
        this.form.content.split('\n').forEach(item => arr.push(`<p>${item.trim()}</p>`))
        this.content = arr.join('')
        this.dialogVisible = true
      },
      async submit () {
        const token = window.sessionStorage.getItem('token')
        const res = await this.$http.post('submit_announcement', { token: token, form: this.form })
          if (res.data.code !== 200) return this.$message.error(res.data.message)
          this.$message({
            message: '发布成功',
            type: 'success'
          })
          return this.$router.push('/admin/announcement')
      }
    }
  }
</script>

<style lang="less" scoped>
.container{
  height: 100%;
  width: 100%;
  padding: 0 17px 47px 0;
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
  margin-top: 24px;
  background-color: #ffffff;
  padding-left: 50%;
  > .el-form{
    padding: 24px;
    width: 520px;
    transform: translate(-50%, 0);
  }
  
}
</style>
<style lang="less">
.dialog-content{
  text-indent: 2em;
}
.dialog-date{
  padding-top: 10px; 
}
</style>
