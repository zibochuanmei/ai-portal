<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { usePortalStore } from './stores/portal'

const portal = usePortalStore()
onMounted(() => portal.loadAgents())
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand-mark"><span class="brand-dot"></span><span>惠中 AI Portal</span></div>
      <p class="side-caption">企业智能工作台</p>
      <nav class="nav-list">
        <RouterLink to="/chat" class="nav-item">对话工作台</RouterLink>
        <RouterLink to="/agents" class="nav-item">我的智能体</RouterLink>
        <RouterLink to="/admin" class="nav-item">管理中心</RouterLink>
      </nav>
      <div class="sidebar-foot">
        <div class="status-pill"><span></span>服务正常</div>
        <div class="user-mini"><div class="avatar">演</div><div><strong>{{ portal.user.display_name }}</strong><small>{{ portal.user.department }}</small></div></div>
      </div>
    </aside>
    <main class="main-area"><RouterView /></main>
  </div>
</template>
