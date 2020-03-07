<template>
  <el-carousel
    indicator-position="outside"
    :autoplay="false"
    height="500px"
  >
    <el-carousel-item
      v-for="item in items"
      :key="item.title"
    >
      <h3>{{ item.title }}</h3>
      <p
        v-for="content in item.content"
        :key="content"
      >
        {{ content }}
      </p>
      <p v-if="item.type===0">
        学生选择开放时间: {{ item.start_time }} - {{ item.end_time }}
      </p>
      <p v-if="item.type===1">
        公示时间: {{ item.start_time }} - {{ item.end_time }}
      </p>
    </el-carousel-item>
  </el-carousel>
</template>

<script>
export default {
  data: function () {
      return {
        items: [1, 2, 3]
      }
  }, 
  async created () {
    this.loading = true
    const token = window.sessionStorage.getItem('token')
    const res = await this.$http.post('get_announcement', { token: token })
    if (res.data.code !== 200) {
      this.$message.error(res.data.message)
    } else {
      this.items = res.data.data.announcements
    }
    this.loading = false
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
.el-carousel__item{
  > p{
    text-align: initial;
    text-indent: 2em;
    padding: 0 40px;
    font-size: 20px;
  }
}
</style>
