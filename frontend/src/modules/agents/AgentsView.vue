<script setup lang="ts">
import { onMounted } from 'vue'
import { usePortalStore } from '../../stores/portal'

const portal = usePortalStore()
onMounted(() => portal.loadAgents())
</script>

<template>
  <section class="page"><header class="topbar"><div><p class="eyebrow">MY AGENTS</p><h1>我的智能体</h1><p class="muted">这里只展示当前身份可以使用的能力。</p></div></header><div class="agent-grid"><article v-for="agent in portal.agents" :key="agent.id" class="agent-card"><div class="card-icon">{{ agent.name.slice(0, 1) }}</div><div class="card-body"><div class="card-heading"><h3>{{ agent.name }}</h3><el-tag size="small" type="success">可用</el-tag></div><p>{{ agent.description }}</p><span>{{ agent.category }}</span></div></article></div></section>
</template>
