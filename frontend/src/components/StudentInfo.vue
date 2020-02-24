<template>
  <div class="container">
    <div class="header">
      个人基本信息
    </div>
    <el-form
      :model="student"
      label-width="80px"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item label="姓名">
            <el-input v-model="student.name" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="学号">
            <el-input v-model="student.id" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="性别">
            <el-input v-model="student.gender" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="年级">
            <el-input v-model="student.grade" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="学院">
            <el-input v-model="student.college" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="专业">
            <el-input v-model="student.subject" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="班级">
            <el-input v-model="student.class_name" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <!-- <el-form-item label="年级">
            <el-input v-model="student.grade" />
          </el-form-item> -->
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      student: {
        name: '',
        id: '',
        gender: '',
        college: '',
        subject: '',
        class_name: ''
        
      }
    }
  }
}
</script>

<style lang="less" scoped>
.container{
  height: 100%;
  background-color: #F1FAFA;
  padding: 0;
}
.header{
  padding: 15px 0 30px;
}
.el-form-item{
  width: 70%;
  margin-left: 15%;
}
</style>
