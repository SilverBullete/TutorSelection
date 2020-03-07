<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>本科导师选择</el-breadcrumb-item>
        <el-breadcrumb-item>选择结果</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        本科学生选择结果
      </div>
    </div>
    <div class="content">
      <el-table
        :data="resultData"
        style="width: 100%"
      >
        <el-table-column
          prop="name"
          label="姓名"
          width="80"
        />
        <el-table-column
          prop="college"
          label="学院"
          min-width="160"
        />
        <el-table-column
          prop="subject"
          label="专业"
          min-width="100"
        />
        <el-table-column
          prop="class_name"
          label="班级"
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
            >
              第一志愿
            </el-tag>
            <el-tag
              v-else=""
              type="info"
              effect="plain"
            >
              第二志愿
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="result"
          label="状态"
          min-width="90"
        >
          <template slot-scope="scope">
            <el-tag
              v-if="scope.row.pass_status==1"
              type="info"
              effect="dark"
            >
              待通过
            </el-tag>
            <el-tag
              v-if="scope.row.pass_status==0"
              type="success"
              effect="dark"
            >
              已通过 
            </el-tag>
            <el-tag
              v-if="scope.row.pass_status==2"
              type="danger"
              effect="dark"
            >
              未通过
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
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
      resultData: [],
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
        this.$http.post('get_selection_res', { token: token }).then(function (res) {
          _this.resultData = res.data.data
        })
        this.loading = false
      },
 methods: {
    showDialog (row) {
        this.studentForm.row = row
        this.dialogVisible = true
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
  > .el-table{
    padding: 24px;
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
