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
      :router="true"
    >
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-message" />公告管理
        </template>
        <el-menu-item-group>
          <el-menu-item
            index="1-1"
            :route="{name:'AnnouncementPublic'}"
          >
            公告发布
          </el-menu-item>
          <el-menu-item-group>
            <el-menu-item
              index="1-2"
              :route="{name:'AAnnouncement'}"
            >
              公告列表
            </el-menu-item>
          </el-menu-item-group>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-user" />学生管理
        </template>
        <el-menu-item-group>
          <el-menu-item
            index="2-1"
            :route="{name:'SInfoManage'}"
          >
            学生信息管理
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">
          <i class="el-icon-menu" />导师管理
        </template>
        <el-menu-item-group>
          <el-menu-item
            index="3-1"
            :route="{name:'TInfoManage'}"
          >
            导师信息管理
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="4">
        <template slot="title">
          <i class="el-icon-s-order" />系统管理
        </template>
        <el-menu-item-group>
          <el-submenu index="4-1">
            <template slot="title">
              一二轮选择
            </template>
            <el-menu-item
              index="4-1-1"
              :route="{name: 'RoundOpen'}"
            >
              一二轮选择开放
            </el-menu-item>
            <el-menu-item
              index="4-1-2"
              :route="{name: 'RoundRes'}"
            >
              一二轮选择结果
            </el-menu-item>
          </el-submenu>
          <el-submenu index="4-2">
            <template slot="title">
              管理员分配
            </template>
            <el-menu-item
              index="4-2-1"
              :route="{name: 'AdminDistribution'}"
            >
              管理员自动分配
            </el-menu-item>
            <el-menu-item
              index="4-2-2"
              :route="{name: 'TeacherConfirmRes'}"
            >
              导师确认情况
            </el-menu-item>
          </el-submenu>
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
