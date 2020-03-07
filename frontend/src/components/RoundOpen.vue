<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>系统管理</el-breadcrumb-item>
        <el-breadcrumb-item>一二轮选择</el-breadcrumb-item>
        <el-breadcrumb-item>一二轮选择开放</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        一二轮选择开放
      </div>
    </div>
    <div class="content">
      <div class="round_select">
        <span>轮次选择</span>：
        <el-select
          v-model="value"
          placeholder="请选择"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
          />
        </el-select>
      </div>
      <div class="date_picker">
        <span>学生选择时间</span>：
        <el-date-picker
          v-model="studentDate"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          align="right"
        />
      </div>
      <div class="submit">
        <el-button
          type="primary"
          @click="submit"
        >
          提交
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      options: [{
        label: '第一轮选择',
        value: '1'
      }, {
        label: '第二轮选择',
        value: '2',
        disabled: true
      }],
      value: '',
      studentDate: ''
    }
  },
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        this.$http.post('admin/get_round_selection', { token: token }).then(function (res) {
          _this.options = res.data.data.options
        })
        this.loading = false
      },
 methods: {
      async submit () {
        const token = window.sessionStorage.getItem('token')
        const res = await this.$http.post('admin/open_selection', { token: token, round: this.value, studentDate: this.studentDate })
        if (res.data.code !== 200) return this.$message.error(res.data.message)
        this.$alert('是否去发布公告提醒同学和老师', '提示', {
          confirmButtonText: '确定',
          callback: action => {
            return this.$router.push('/admin/announcement')
          }
        })
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
  > .date_picker{
      padding-bottom: 24px;
      font-size: 18px;
  }
  > .submit{
      padding-bottom: 24px;
  }
  > .round_select{
    padding: 24px;
    > span{
      letter-spacing: 9px;
    }
    font-size: 18px;
    > .el-select{
      width: 400px;
    }
  }
}

</style>
