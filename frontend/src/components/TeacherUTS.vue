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
          :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
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
            sortable
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
            min-width="100"
          />
          <el-table-column
            label="简历"
            min-width="80"
          >
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
          <el-table-column
            label="志愿"
            min-width="90"
          >
            <template slot-scope="scope">
              <el-tag
                v-if="scope.row.type"
                type=""
                effect="plain"
                size="small"
              >
                第一志愿
              </el-tag>
              <el-tag
                v-else=""
                type="info"
                effect="plain"
                size="small"
              >
                第二志愿
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
                placeholder="搜索学生姓名"
              />
            </template>
            <template slot-scope="scope">
              <el-button
                v-if="isInArray(select, scope.row.id)"
                size="mini"
                type="primary"
                @click="Select(scope.row)"
              >
                选择
              </el-button>
              <el-button
                v-else=""
                size="mini"
                type="primary"
                plain
                @click="Select(scope.row)"
              >
                选择
              </el-button>
              <el-button
                v-if="isInArray(unSelect, scope.row.id)"
                size="mini"
                type="danger"
                @click="UnSelect(scope.row)"
              >
                不选择
              </el-button>
              <el-button
                v-else=""
                size="mini"
                type="danger"
                plain
                @click="UnSelect(scope.row)"
              >
                不选择
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="submit">
          <div class="btn">
            <a
              :href="'http://localhost:8001/api/teacher/export?token='+token"
            >
              <el-button>
                导出
              </el-button></a>
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
          <el-button
            v-if="isInArray(select, studentForm.row.id)"
            type="primary"
            @click="Select(studentForm.row)"
          >
            选择
          </el-button>
          <el-button
            v-else=""
            type="primary"
            plain
            @click="Select(studentForm.row)"
          >
            选择
          </el-button>
          <el-button
            v-if="isInArray(unSelect, studentForm.row.id)"
            type="danger"
            @click="UnSelect(studentForm.row)"
          >
            不选择
          </el-button>
          <el-button
            v-else=""
            type="danger"
            plain
            @click="UnSelect(studentForm.row)"
          >
            不选择
          </el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-extend-native
Array.prototype.remove = function (val) {
  var index = this.indexOf(val)
  if (index > -1) {
  this.splice(index, 1)
  }
}

export default {
  data () {
    return {
      maxNum: 0,
      select: [],
      unSelect: [],
      tableData: [],
      token: '',
      search: '',
      dialogVisible: false,
      studentForm: {
        row: ''
      }
    }
  },
  created () {
    this.loading = true
    const _this = this
    const token = window.sessionStorage.getItem('token')
    this.token = token
    this.$http.post('teacher/get_students', { token: token }).then(function (res) {
      _this.tableData = res.data.data.students
      _this.maxNum = res.data.data.maxNum
    })
    this.loading = false
  },
  methods: {
    update () {
      const _this = this
      this.$http.post('teacher/update_students', { token: this.token, select: this.select, unSelect: this.unSelect }).then(function (res) {
        _this.tableData = res.data.data.students
        _this.select = res.data.data.select
        _this.unSelect = res.data.data.unSelect
      })
    },
    showDialog (row) {
      this.studentForm.row = row
      this.dialogVisible = true
    },
    Select (row) {
      if (this.select.length >= this.maxNum) {
        this.$message.error('抱歉，您选择的学生已达上限！')
      } else {
        if (this.isInArray(this.select, row.id)) {
          this.$confirm('你确定将' + row.name + '从你的不选择列表中移除吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
          }).then(() => {
            this.$message({
              type: 'success',
              message: '移除成功！'
            })
            this.select.remove(row.id)
            this.update()
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已撤销选择'
            })          
          })
        } else {
          this.select.push(row.id)
          this.unSelect.remove(row.id)
          this.$message({
              type: 'success',
              message: '选择成功！'
            })
          this.update()
        }
      }
      this.dialogVisible = false
    },
    UnSelect (row) {
      if (this.isInArray(this.unSelect, row.id)) {
        this.$confirm('你确定将' + row.name + '从你的学生中移除吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '移除成功！'
          })
          this.unSelect.remove(row.id)
          this.update()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已撤销选择'
          })          
        })
      } else {
        this.unSelect.push(row.id)
        this.select.remove(row.id)
        this.$message({
            type: 'success',
            message: '操作成功！(不选择的学生将出现在表格的底部)'
          })
        this.update()
      }
      this.dialogVisible = false
    },
    async submit () {
      const res = await this.$http.post('teacher/submit_selections', { token: this.token, select: this.select, unSelect: this.unSelect })
      if (res.data.data.result) {
        this.$message({
          type: 'success',
          message: res.data.data.message
        })
      } else {
        this.$message.error('修改失败')
      }
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
    text-align: initial;
  }
  
</style>
