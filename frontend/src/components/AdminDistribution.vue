<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>系统管理</el-breadcrumb-item>
        <el-breadcrumb-item>管理员分配</el-breadcrumb-item>
        <el-breadcrumb-item>管理员自动分配</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        管理员自动分配
      </div>
    </div>
    <div class="content">
      <div class="button-group">
        <div class="left">
          <el-button
            type="primary"
            @click="automatically_assign_teacher"
          >
            自动分配导师
          </el-button>
        </div>
        <div class="right">
          <el-button
            type="primary"
            @click="submit"
          >
            提交
          </el-button>
        </div>
      </div>
      <div class="table">
        <el-table
          v-loading="loading"
          :data="tableData.filter(function(row){
            if (!search){
              return row
            } else {
              return Object.keys(row).some(function (key) {
                return String(row[key]).toLowerCase().indexOf(search) > -1
              })
            }
          })"
          stripe
          style="width: 100%"
          max-height="600"
        >
          <el-table-column
            prop="name"
            label="姓名"
            min-width="70"
          />
          <el-table-column
            prop="id"
            label="学号"
            min-width="120"
          />
          <el-table-column
            prop="class_name"
            label="班级"
            min-width="150"
          />
          <el-table-column 
            prop="assigned_teacher"
            label="分配导师"
            min-width="100"
          />
          <el-table-column
            align="right"
            min-width="180"
          >
            <template
              slot="header"
              slot-scope="scope"
            >
              <el-input
                v-model="search"
                size="mini"
                placeholder="搜索关键词"
              />
            </template>
            <template slot-scope="scope">
              <el-button
                :href="scope.row.profile"
                type="text"
                @click="showDialog(scope.row)"
              >
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
        tableData: [],
        search: '',
        dialogVisible: false,
        studentForm: {
            row: ''
        },
        loading: false
    }
  },
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        this.$http.post('admin/get_no_action_students', { token: token }).then(function (res) {
        _this.tableData = res.data.data.students
        })
        this.loading = false
      },
 methods: {
     showDialog (row) {
      this.studentForm.row = row
      this.dialogVisible = true
    },
     automatically_assign_teacher () {
        this.loading = true
        const token = window.sessionStorage.getItem('token')
        const _this = this
        this.$http.post('admin/automatically_assign_teacher', { token: token }).then(function (res) {
          if(res.data.code==500){
            _this.$message.error(res.data.message);
          }else{
            _this.tableData = res.data.data.students
          }
          _this.loading = false
        })
      },
      async submit () {
        const token = window.sessionStorage.getItem('token')
        const { data: res } = await this.$http.post('admin/submit_distribution', { token: token, tableData: this.tableData })
        if (res.code !== 200) return this.$message.error(res.message)
        this.$alert('记得提醒老师确认', '提示', {
            confirmButtonText: '确定',
            callback: action => {
                return this.$router.push('/admin/teacher_confirm_res')
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
  .button-group{
    display: flex;
    justify-content: space-between;
    padding: 24px 24px 0 24px;
  }
  background-color: #ffffff;
  .table{
    margin: 0 24px;
    padding: 24px 0;
  }
  .submit{
    padding-bottom: 24px;
    padding-top: 24px;
    > .btn{
      display: flex;
      justify-content: flex-end;
      padding-right: 30px;
      > .el-button{
        margin-left: 20px;
      }
    }
  }
}

</style>
