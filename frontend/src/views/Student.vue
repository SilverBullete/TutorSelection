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
      <studentAside />
      <el-scrollbar>
        <el-main>
          <component :is="currentMenuComponent" />
        </el-main>
      </el-scrollbar>
    </el-container>
  </el-container>
</template>

<script>
    import studentAside from '../components/Aside.vue'
    import studentInfo from '../components/StudentInfo'
    import studentResume from '../components/StudentResume'
    import studentUTS from '../components/StudentUTS'
    export default {
        components: { studentAside, studentInfo, studentResume, studentUTS },
        data: function () {
            return {
                currentMenuComponent: studentUTS
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
    // width: 100%;
    padding: 0 24px 24px 24px;
    background-color: #F0F2F5;
}
</style>
