<template>
  <el-container class="login-container">
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
      <el-main>
        <el-carousel height="500px">
          <el-carousel-item
            v-for="item in 4"
            :key="item"
          >
            <h3 />
          </el-carousel-item>
        </el-carousel>
      </el-main>
      <el-aside
        class="loginForm-container"
        width="500px"
      >
        <loginForm />
      </el-aside>
    </el-container>
  </el-container>
</template>

<script>
    import loginForm from '../components/LoginForm.vue'
    export default {
        components: { loginForm }
    }
</script>

<style lang="less" scoped>
.el-header{
    background-color: #DDDDDD;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 20px;
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
.login-container{
    height: 100%;
}
.loginForm-container{
    position: absolute;
    right: 0px;
    top: 60px;
    height: 100%;
    min-height: 410px;
    margin-bottom: -60px;
}
.el-main{
    margin-right: 500px;
}

  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
</style>
