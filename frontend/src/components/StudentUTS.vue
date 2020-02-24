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
          :options="options"
          :props="{ multiple: true, checkStrictly: true, expandTrigger: 'hover' }"
          collapse-tags
          clearable
        />
      </div>
      <div class="institute">
        <el-tag
          v-for="tag in tags"
          :key="tag.name"
          closable
          :type="tag.type"
          @click="open"
        >
          {{ tag.name }}
        </el-tag>
      </div>
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
                href="https://element.eleme.io"
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
                size="mini"
                type="primary"
                @click="handleEdit(scope.$index, scope.row)"
              >
                第一导师
              </el-button>
              <el-button
                size="mini"
                type=""
                @click="handleDelete(scope.$index, scope.row)"
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
      options: [
        {
          value: 'zhinan',
          label: '计算机科学与技术学院、软件学院',
          children: [{
            value: 'shejiyuanze',
            label: '计算机智能系统研究所'
          }]
        }, {
          value: 'zhinan',
          label: '计算机科学与技术学院、软件学院',
          children: [{
            value: 'shejiyuanze',
            label: '计算机智能系统研究所2'
          }]
        }
      ],
      tags: [
        { name: '计算机智能系统研究所', type: 'info' }
      ],
      tableData: [{
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }, {
          name: '沈国江',
          college: '计算机科学与技术学院、软件学院',
          institute: '计算机智能系统研究所',
          subject: '智慧城市、智能交通系统、大数据技术'
        }],
        search: ''
    }
  },
  methods: {
      open () {
        this.$alert('这是一段内容', '标题名称', {
          confirmButtonText: '确定',
          callback: action => {
          }
        })
      },
      handleEdit (index, row) {
        console.log(index, row)
      },
      handleDelete (index, row) {
        console.log(index, row)
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
    padding-bottom: 20px;
    > .btn{
      display: flex;
      justify-content: flex-end;
      padding-right: 30px;
    }
  }
}

</style>
