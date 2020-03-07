<template>
  <div class="container">
    <div class="header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>导师管理</el-breadcrumb-item>
        <el-breadcrumb-item>导师信息管理</el-breadcrumb-item>
      </el-breadcrumb>
      <div class="header-heading">
        导师信息管理
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
          @click="open(tag.name)"
        >
          {{ tag.name }}
        </el-tag>
      </div>
      <div class="table">
        <el-table
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
  </div>
</template>

<script>
export default {
  data () {
    return {
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
    this.$http.post('admin/teachers', { token: token }).then(function (res) {
      _this.tableData = res.data.data.teachers
      _this.options = res.data.data.options
    })
    this.loading = false
  },
  methods: {
    async open (name) {
      const res = await this.$http.post('get_institute_info', { institute: name })
      if (res.data.code !== 200) return this.$message.error(res.data.message)
      this.$alert(res.data.data.info, '研究机构简介', {
        confirmButtonText: '确定',
        callback: action => {
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
        this.$http.post('admin/teachers_by_institute', { token: token, institutes: institutes }).then(function (res) {
          _this.tableData = res.data.data.teachers
        }) 
      } else {
        this.$http.post('admin/teachers', { token: token }).then(function (res) {
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
    padding-bottom: 24px;
  }
}

</style>
