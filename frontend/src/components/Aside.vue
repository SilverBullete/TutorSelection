<template>
  <el-aside
    width="220px"
    style="background-color: #001529"
  >
    <el-menu
      :default-openeds="['2','3','4']"
      background-color="#001529"
      text-color="#ffffff"
      active-text-color="#ffffff"
    >
      <el-menu-item index="1">
        <template slot="title">
          <i class="el-icon-message" />公告
        </template>
      </el-menu-item>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-user" />个人信息
        </template>
        <el-menu-item-group>
          <el-menu-item index="2-1">
            个人基本信息
          </el-menu-item>
          <el-menu-item index="2-2">
            个人简历
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">
          <i class="el-icon-menu" />本科导师选择
        </template>
        <el-menu-item-group>
          <el-menu-item index="3-1">
            导师选择
          </el-menu-item>
          <el-menu-item index="3-2">
            选择情况
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="4">
        <template slot="title">
          <i class="el-icon-s-order" />毕页设计导师选择
        </template>
        <el-menu-item-group>
          <el-menu-item index="4-1">
            导师选择
          </el-menu-item>
          <el-menu-item index="4-2">
            选择情况
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
    
}
</script>

<style lang="less" scoped>
.el-aside{
  height: 100%;
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
  z-index: 10;
  text-align: left;
}
.el-menu-item.is-active{
  background-color: #1890ff!important;
}
</style>
