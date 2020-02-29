<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>本科导师选择</el-breadcrumb-item>
        <el-breadcrumb-item>学生选择</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        本科学生选择
      </div>
    </div>
    <div class="content">
      <div class="table">
        <el-table
          :data="tableData"
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
            prop="college"
            label="学院"
            min-width="180"
          />
          <el-table-column
            prop="subject"
            label="专业"
            min-width="150"
          />
          <el-table-column
            prop="gpa"
            label="绩点"
            min-width="100"
            sortable
          />
          <el-table-column
            prop="rank"
            label="绩点排名"
            min-width="130"
          />
          <el-table-column
            label="简历"
            min-width="100"
          >
            <template slot-scope="scope">
              <el-link
                :href="scope.row.profile"
                target="_blank"
                type="primary"
              >
                查看详情
              </el-link>
            </template>
          </el-table-column>
          <el-table-column
            align="right"
            min-width="220"
          >
            <template
              slot="header"
            >
              <el-button
                size="mini"
                type="primary"
                @click="Export"
              >
                导出
              </el-button>
            </template>
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                @click="Select(scope.row)"
              >
                选择
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="submit">
          <div class="btn">
            <el-button
              type="primary"
              @click="submit"
            >
              提交
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      select: [],
      options: [],
      tags: [],
      tableData: [],
      search: ''
    }
  },
  created () {
    this.loading = true
    const _this = this
    const token = window.sessionStorage.getItem('token')
    this.$http.post('student/get_teachers', { token: token }).then(function (res) {
      _this.select = [res.data.data.select[0], res.data.data.select[1]]
      _this.tableData = res.data.data.teachers
      _this.options = res.data.data.options
    })
    this.loading = false
  },
  methods: {
    submit () {
      const token = window.sessionStorage.getItem('token')
      this.$http.post('student/update_selection', { token: token, select: this.select }).then(function (res) {
        if (res.data.data.result) {
          this.$message({
            type: 'success',
            message: res.data.data.message
          })
        } else {
          this.$message.error('修改失败')
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
  // margin: 0 -24px;
  background-color: #ffffff;
  .select{
    display: flex;
    margin-top: 24px;
    padding: 10px 20px;
    align-items: center;
    > span{
      font-size: 16px;
      padding-right: 10px;
    }
  }
  .institute{
    display: flex;
    padding: 15px;
    .el-tag + .el-tag {
      margin-left: 10px;
    }
  }
  .table{
    margin: 0 24px;
  }
  .submit{
    padding-bottom: 24px;
    padding-top: 24px;
    > .btn{
      display: flex;
      justify-content: flex-end;
      padding-right: 30px;
    }
  }
}

</style>
