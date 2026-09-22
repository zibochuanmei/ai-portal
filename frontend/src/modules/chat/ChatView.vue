<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../../api/client'
import { usePortalStore } from '../../stores/portal'

const portal = usePortalStore()
const selectedAgent = ref('document-assistant')
const message = ref('')
const answer = ref('')
const sending = ref(false)
const activeAgent = computed(() => portal.agents.find((item) => item.id === selectedAgent.value))

async function sendMessage() {
  if (!message.value.trim()) return
  sending.value = true
  try {
    const { data } = await api.post('/api/v1/agent-runs', { agent_id: selectedAgent.value, message: message.value })
    answer.value = data.answer
    message.value = ''
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section class="page chat-page">
    <header class="topbar"><div><p class="eyebrow">AI WORKSPACE</p><h1>今天需要处理什么？</h1><p class="muted">选择一个已授权的智能体，上传资料并直接描述你的目标。</p></div><el-tag type="success" effect="light">技术部 · 员工</el-tag></header>
    <div class="chat-layout">
      <div class="conversation-panel">
        <div v-if="!answer" class="empty-chat"><div class="empty-icon">✦</div><h2>让 AI 帮你完成一项工作</h2><p>例如：整理这份会议纪要，提取待办事项并按负责人分组。</p></div>
        <div v-else class="answer-card"><div class="answer-label">{{ activeAgent?.name }}</div><p>{{ answer }}</p><small>演示结果 · 后续将接入真实模型和引用链</small></div>
        <div class="composer"><div class="composer-toolbar"><el-select v-model="selectedAgent" size="small" style="width: 190px"><el-option v-for="agent in portal.agents" :key="agent.id" :label="agent.name" :value="agent.id" /></el-select><span class="toolbar-hint">主控 Agent 将在后续版本自动路由</span></div><div class="input-row"><el-input v-model="message" type="textarea" :rows="3" resize="none" placeholder="告诉智能体你需要什么，支持上传 PDF、Word、TXT 或图片" @keydown.enter.exact.prevent="sendMessage" /><el-button type="primary" :loading="sending" @click="sendMessage">发送</el-button></div></div>
      </div>
      <aside class="quick-panel"><p class="eyebrow">已授权能力</p><div v-for="agent in portal.agents" :key="agent.id" class="quick-agent" :class="{ active: selectedAgent === agent.id }" @click="selectedAgent = agent.id"><div class="agent-icon">{{ agent.name.slice(0, 1) }}</div><div><strong>{{ agent.name }}</strong><small>{{ agent.category }}</small></div></div><div class="permission-note">权限由平台统一控制，主控 Agent 只能调用你已获授权的子 Agent。</div></aside>
    </div>
  </section>
</template>
