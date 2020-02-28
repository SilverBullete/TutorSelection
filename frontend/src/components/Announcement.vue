<template>
  <el-carousel
    indicator-position="outside"
    :autoplay="false"
    height="500px"
  >
    <el-carousel-item
      v-for="item in items"
      :key="item"
    >
      <h3>{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<script>
export default {
  data: function () {
      return {
        items: [1, 2, 3]
      }
  }    
}
</script>

<style lang="less" scoped>
.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}
  
.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}
.el-carousel{
  margin-top: 24px;
}
</style>
