<template>
  <el-container>
    <el-header>
      <div>
        <img
          src="../assets/zjut.png"
          alt=""
        >
        <span>浙江工业大学导师双向选择系统</span>
      </div>
    </el-header>
    <el-container>
      <teacherAside />
      <el-scrollbar>
        <el-main>
          <transition name="teacher">
            <router-view />
          </transition>
        </el-main>
      </el-scrollbar>
    </el-container>
  </el-container>
</template>

<script>
import teacherAside from '../components/TeacherAside.vue'

export default {
    components: { teacherAside },
    data: function () {
        return {
            
        }
    }
}
</script>

<style lang="less" scoped>
.el-header{
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
    position: relative;
    background-color: #F4F7ED;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 20px;
    border: 1px solid #E4E4E4;
    > div {
        display: flex;
        align-items: center;
        > img{
            height: 40px;
            width: 40px;
        }
        > span{
            margin-left: 10px;
        }
    }
}
.el-container{
    height: 100%;
}
.el-main{
    width: 100%;
    height: 100%;
    padding: 0 24px 24px 24px;
    background-color: #F0F2F5;
}
.el-scrollbar{
    height: 100%;
    width: 100%;
    background-color: #F0F2F5;
}
</style>
