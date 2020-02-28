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
        本科导师选择结果
      </div>
    </div>
    <div class="content">
      <el-table
        :data="resultData"
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <el-table-column
          prop="type"
          label="导师志愿"
          width="80"
        />
        <el-table-column
          prop="name"
          label="姓名"
          width="80"
        />
        <el-table-column
          prop="college"
          label="学院"
          min-width="180"
        />
        <el-table-column
          prop="institute"
          label="研究机构"
          min-width="150"
        />
        <el-table-column
          prop="subject"
          label="研究方向"
          min-width="220"
        />
        <el-table-column
          prop="result"
          label="研究成果"
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
          prop="result"
          label="状态"
        >
          <template slot-scope="scope">
            <el-tag
              v-if="scope.row.pass_status==0"
              type="info"
              effect="dark"
            >
              待通过
            </el-tag>
            <el-tag
              v-if="scope.row.pass_status==1"
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
  </div>
</template>

<script>
export default {
  data () {
    return {
      resultData: []
    }
  },
  created () {
        this.loading = true
        const _this = this
        const token = window.sessionStorage.getItem('token')
        this.$http.post('student/get_selection_res', { token: token }).then(function (res) {
          _this.resultData = res.data.data
        })
        this.loading = false
      },
 methods: {
      tableRowClassName ({ row, rowIndex }) {
        if (row.pass_status === 2) {
          return 'warning-row'
        } else if (row.pass_status === 1) {
          return 'success-row'
        }
        return ''
      }
    }
  }
</script>

<style lang="less">
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
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
}

</style>
