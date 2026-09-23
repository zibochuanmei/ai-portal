<script setup lang="ts">
import { onMounted } from 'vue'
import { usePortalStore } from '../../stores/portal'

const portal = usePortalStore()
onMounted(() => portal.loadWorkflows())
</script>

<template>
  <section class="page"><header class="topbar"><div><p class="eyebrow">MY WORKFLOWS</p><h1>我的工作流</h1><p class="muted">这里只展示当前身份已经获授权的业务能力。</p></div></header><div v-if="portal.error" class="error-banner">{{ portal.error }}</div><div class="agent-grid"><article v-for="workflow in portal.workflows" :key="workflow.workflow_id" class="agent-card"><div class="card-icon">{{ workflow.name.slice(0, 1) }}</div><div class="card-body"><div class="card-heading"><h3>{{ workflow.name }}</h3><el-tag size="small" type="success">可用</el-tag></div><p>{{ workflow.description }}</p><span>{{ workflow.category }}</span></div></article></div></section>
</template>
