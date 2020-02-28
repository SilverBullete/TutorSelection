<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>本科导师选择</el-breadcrumb-item>
        <el-breadcrumb-item>导师选择</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        本科导师选择
      </div>
    </div>
    <div class="content">
      <div class="select">
        <span class="demonstration">信息筛选</span>
        <el-cascader
          ref="myCascader"
          placeholder="搜索研究机构"
          :options="options"
          :props="{ multiple: true, expandTrigger: 'hover' }"
          clearable
          filterable
          @change="change"
        />
      </div>
      <div class="institute">
        <el-tag
          v-for="tag in tags"
          :key="tag.name"
          type="info"
          @click="open"
        >
          {{ tag.name }}
        </el-tag>
      </div>
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
            align="right"
            min-width="220"
          >
            <template
              slot="header"
            >
              <el-input
                v-model="search"
                size="small"
                placeholder="搜索姓名或研究方向"
              />
            </template>
            <template slot-scope="scope">
              <el-button
                v-if="select[0] === scope.row.id"
                size="mini"
                type="primary"
                @click="revoke(scope.row)"
              >
                第一导师
              </el-button>
              <el-button
                v-else=""
                size="mini"
                type="primary"
                plain
                @click="first(scope.row)"
              >
                第一导师
              </el-button>
              <el-button
                v-if="select[1] === scope.row.id"
                size="mini"
                type="info"
                @click="revoke(scope.row)"
              >
                第二导师
              </el-button>
              <el-button
                v-else=""
                size="mini"
                type="info"
                plain
                @click="second(scope.row)"
              >
                第二导师
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
    open () {
      this.$alert('这是一段内容', '标题名称', {
        confirmButtonText: '确定',
        callback: action => {
        }
      })
    },
    updateData () {
      console.log(this.select)
      const nodes = this.$refs.myCascader.getCheckedNodes(true)
      const institutes = []
      nodes.forEach(node => {
        institutes.push(node.value)
      })
      const _this = this
      const token = window.sessionStorage.getItem('token')
      if (institutes.length) {
        this.$http.post('student/get_teachers_by_institute', { token: token, institutes: institutes, select: this.select }).then(function (res) {
        _this.tableData = res.data.data.teachers
      }) 
      } else {
        this.$http.post('student/get_teachers', { token: token, select: this.select }).then(function (res) {
          _this.tableData = res.data.data.teachers
        })
      }
    },
    first (row) {
      var message = ''
      var change = false
      if (row.id === this.select[1]) {
        message = '你已选择' + row.name + '老师作为你的第二志愿导师，是否将其替换为第一志愿导师？'
        change = true
      } else if (this.select[0]) {
        message = '你确定选择' + row.name + '老师替代' + this.tableData[0].name + '老师作为你的第一志愿导师吗？'
      } else {
        message = '你确定选择' + row.name + '老师作为你的第一志愿导师吗？'
      }
      this.$confirm(message, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '选择成功！注意提交保存修改！'
          })
          if (change) {
            if (this.select[0]) {
              this.select[1] = this.select[0]
            } else {
              this.select[1] = ''
            }
          }
          this.select[0] = row.id
          this.updateData()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已撤销选择'
          })          
        })
    },
    second (row) {
      var message = ''
      var change = false
      if (row.id === this.select[0]) {
        message = '你已选择' + row.name + '老师作为你的第一志愿导师，是否将其替换为第二志愿导师？'
        change = true
      } else if (this.select[1] && this.select[0]) {
        message = '你确定选择' + row.name + '老师替代' + this.tableData[1].name + '老师作为你的第二志愿导师吗？'
      } else if (this.select[1]) {
        message = '你确定选择' + row.name + '老师替代' + this.tableData[0].name + '老师作为你的第二志愿导师吗？'
      } else {
        message = '你确定选择' + row.name + '老师作为你的第二志愿导师吗？'
      }
      this.$confirm(message, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '选择成功！注意提交保存修改！'
          })
          if (change) {
            if (this.select[1]) {
              this.select[0] = this.select[1]
            } else {
              this.select[0] = ''
            }
          }
          this.select[1] = row.id
          this.updateData()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已撤销选择'
          })          
        })
    },
    revoke (row) {
      var message = ''
      var index = -1
      if (row.id === this.select[0]) {
        index = 0
        message = '是否确定取消选择' + row.name + '老师作为你的第一志愿导师'
      } else {
        index = 1
        message = '是否确定取消选择' + row.name + '老师作为你的第二志愿导师'
      }
      this.$confirm(message, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '选择成功！注意提交保存修改！'
          })
          this.select[index] = '' 
          this.updateData()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已撤销选择'
          })          
        })
    },
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
    },
    change (items) {
      const tags = []
      const institutes = []
      items.forEach(node => {
          tags.push({ name: node[1] })
          institutes.push(node[1])
      })
      this.tags = tags
      const _this = this
      const token = window.sessionStorage.getItem('token')
      if (institutes.length) {
        this.$http.post('student/get_teachers_by_institute', { token: token, institutes: institutes, select: this.select }).then(function (res) {
          _this.tableData = res.data.data.teachers
        }) 
      } else {
        this.$http.post('student/get_teachers', { token: token, select: this.select }).then(function (res) {
          _this.tableData = res.data.data.teachers
        })
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
