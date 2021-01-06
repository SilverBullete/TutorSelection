<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>系统管理</el-breadcrumb-item>
        <el-breadcrumb-item>管理员分配</el-breadcrumb-item>
        <el-breadcrumb-item>导师确认情况</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        导师确认情况
      </div>
    </div>
    <div class="content">
      <div class="button-group">
        <div class="left">
          <el-button
            type="primary"
            @click="get_teacher"
          >
            筛选未处理的导师
          </el-button>
          <el-button
            type="primary"
            @click="get_back"
          >
            返回选择结果
          </el-button>
        </div>
        <el-button
          v-if="!isFinished"
          type="primary"
          @click="this.$router.push('/admin/admin_distribution')"
        >
          管理员分配
        </el-button>
        <el-button
          v-else=""
          type="primary"
          @click="this.$router.push('/admin/announcement_public')"
        >
          进入公示阶段
        </el-button>
      </div>
      <div class="table">
        <el-table
          v-if="!teacherTable"
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
            prop="first_aspiration"
            label="第一志愿"
            min-width="100"
          />
          <el-table-column
            prop="first_res"
            label="第一志愿结果"
            min-width="100"
          >
            <template slot-scope="scope">
              <el-tag
                v-if="scope.row.first_res==='通过'"
                type="success"
              >
                {{ scope.row.first_res }}
              </el-tag>
              <el-tag
                v-if="scope.row.first_res==='未通过'"
                type="danger"
              >
                {{ scope.row.first_res }}
              </el-tag>
              <el-tag
                v-if="scope.row.first_res==='待通过'"
                type="info"
              >
                {{ scope.row.first_res }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="second_aspiration"
            label="第二志愿"
            min-width="100"
          /><el-table-column
            prop="second_res"
            label="第二志愿结果"
            min-width="100"
          >
            <template slot-scope="scope">
              <el-tag
                v-if="scope.row.second_res==='通过'"
                type="success"
              >
                {{ scope.row.second_res }}
              </el-tag>
              <el-tag
                v-if="scope.row.second_res==='未通过'"
                type="danger"
              >
                {{ scope.row.second_res }}
              </el-tag>
              <el-tag
                v-if="scope.row.second_res==='待通过'"
                type="info"
              >
                {{ scope.row.second_res }}
              </el-tag>
            </template>
          </el-table-column>
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
        <el-table
          v-else=""
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
            prop="college"
            label="学院"
            min-width="240"
          />
          <el-table-column
            prop="institute"
            label="研究机构"
            min-width="200"
          />
          <el-table-column
            prop="subject"
            label="研究方向"
            min-width="220"
          />
          <el-table-column
            align="right"
            min-width="200"
          >
            <template
              slot="header"
              slot-scope="scope"
            >
              <el-input
                v-model="search"
                size="small"
                placeholder="搜索关键词"
              />
            </template>
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
        </el-table>
      </div>
    </div>
    <div class="dialog">
      <el-dialog
        title="学生简历"
        :visible.sync="dialogVisible"
      >
        <el-form
          :model="studentForm"
          label-width="80px"
        >
          <el-row :gutter="24">
            <el-col :span="16">
              <p>姓名: <span class="info">{{ studentForm.row.name }}</span></p>
              <p>专业: <span class="info">{{ studentForm.row.subject }}</span></p>
              <p>绩点: <span class="info">{{ studentForm.row.gpa }}</span></p>
              <p>电话: <span class="info">{{ studentForm.row.phone }}</span></p>
              <p>邮箱: <span class="info">{{ studentForm.row.email }}</span></p>
              <p>是否接受分配: <span class="info">{{ studentForm.row.agree_distribution }}</span></p>
            </el-col>
            <el-col :span="8">
              <el-image :src="studentForm.row.avatar">
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
            </el-col>
          </el-row>
          <el-form-item label="个人简介">
            <el-input
              v-model="studentForm.row.profile"
              type="textarea"
              :rows="6"
            />
          </el-form-item>
          <el-form-item label="获奖情况">
            <el-input
              v-model="studentForm.row.award"
              type="textarea"
              :rows="6"
            />
          </el-form-item>
        </el-form>
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
      tableData: [],
      search: '',
      dialogVisible: false,
      studentForm: {
        row: ''
      },
      teacherTable: false,
      isFinished: false
    }
  },
  created () {
    this.loading = true
    const _this = this
    const token = window.sessionStorage.getItem('token')
    this.$http.post('admin/get_teacher_confirm_res', { token: token }).then(function (res) {
      _this.tableData = res.data.data.students
      _this.isFinished = res.data.data.isFinished
    })
    this.loading = false
  },
  methods: {
    showDialog (row) {
      this.studentForm.row = row
      this.dialogVisible = true
    },
    get_teacher () {
      const _this = this
      const token = window.sessionStorage.getItem('token')
      this.$http.post('admin/get_no_action_teachers', { token: token }).then(function (res) {
        if(res.data.code==500){
            _this.$message.error(res.data.message);
          }else{
          _this.tableData = res.data.data.teachers;
          _this.teacherTable = true
        }
      })
    }, 
    get_back () {
      const _this = this
      const token = window.sessionStorage.getItem('token')
      this.$http.post('admin/get_teacher_confirm_res', { token: token }).then(function (res) {
        if(res.data.code==500){
            _this.$message.error(res.data.message);
          }else{
          _this.tableData = res.data.data.students
          _this.teacherTable = false
          _this.isFinished = res.data.data.isFinished
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
.el-image{
  width: 100px;
  margin-top: -10px;
}
.info{
    padding-left: 10px;
}
</style>
<style lang="less">
.el-form{
    > .el-row{
      text-align: left!important;
      padding-left: 37px;
    }
  }
  .el-dialog__body{
    padding: 0 20px!important;
  }
  
</style>
