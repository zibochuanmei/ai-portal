<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { usePortalStore } from './stores/portal'

const portal = usePortalStore()
onMounted(async () => {
  try {
    await portal.loadCurrentUser()
    await portal.loadWorkflows()
  } catch {
    portal.error = '暂时无法连接 AI Portal，请检查后端服务。'
  }
})
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand-mark"><span class="brand-dot"></span><span>惠中 AI Portal</span></div>
      <p class="side-caption">企业智能工作台</p>
      <nav class="nav-list">
        <RouterLink to="/chat" class="nav-item">对话工作台</RouterLink>
        <RouterLink to="/agents" class="nav-item">我的工作流</RouterLink>
        <RouterLink v-if="portal.user.role === 'platform_admin'" to="/admin" class="nav-item">管理中心</RouterLink>
      </nav>
      <div class="sidebar-foot">
        <div class="status-pill"><span></span>{{ portal.error ? '连接异常' : '服务正常' }}</div>
        <div class="user-mini"><div class="avatar">{{ portal.user.display_name.slice(0, 1) }}</div><div><strong>{{ portal.user.display_name }}</strong><small>{{ portal.user.department }}</small></div></div>
      </div>
    </aside>
    <main class="main-area"><RouterView /></main>
  </div>
</template>
