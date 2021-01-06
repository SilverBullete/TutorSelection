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
        <el-carousel height="800px">
          <el-carousel-item
            v-for="item in items"
            :key="item.src"
          >
            <div
              class="zoomImage"
              :style="{backgroundImage:'url(' + item.src + ')'}"
            />
          </el-carousel-item>
        </el-carousel>
      </el-main>
      <el-aside
        class="loginForm-container"
        width="500px"
      >
        <transition name="main">
          <router-view />
        </transition>
      </el-aside>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data: function () {
      return {
        items: [{
          src: 'http://127.0.0.1:8001/media/bg/bg1.jpg'
        }, {
          src: 'http://127.0.0.1:8001/media/bg/bg2.jpg'
        }, {
          src: 'http://127.0.0.1:8001/media/bg/bg3.jpg'
        }, {
          src: 'http://127.0.0.1:8001/media/bg/bg4.jpg'
        }]
      }
  }
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
  .zoomImage{
    width:100%;
    height:0;
    padding-bottom: 100%;
    overflow:hidden;
    background-position: center center;
    background-repeat: no-repeat;
    -webkit-background-size:cover;
    -moz-background-size:cover;
    background-size:cover;
}
</style>
