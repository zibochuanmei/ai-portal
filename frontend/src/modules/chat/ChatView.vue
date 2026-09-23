<script setup lang="ts">
import { computed, ref } from 'vue'
import { api } from '../../api/client'
import { usePortalStore } from '../../stores/portal'

const portal = usePortalStore()
const selectedWorkflow = ref('')
const message = ref('')
const answer = ref('')
const sending = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const fileIds = ref<string[]>([])
const error = ref('')
const activeWorkflow = computed(() => portal.workflows.find((item) => item.workflow_id === selectedWorkflow.value))

function ensureWorkflow() {
  if (!selectedWorkflow.value && portal.workflows.length > 0) {
    selectedWorkflow.value = portal.workflows[0].workflow_id
  }
}

async function uploadFile(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  error.value = ''
  const form = new FormData()
  form.append('file', file)
  try {
    const { data } = await api.post('/api/v1/files', form)
    fileIds.value = [...fileIds.value, data.file_id]
  } catch {
    error.value = '文件上传失败，请检查格式和大小。'
  } finally {
    input.value = ''
  }
}

async function sendMessage() {
  ensureWorkflow()
  if (!message.value.trim() || !selectedWorkflow.value) return
  sending.value = true
  error.value = ''
  try {
    const { data } = await api.post(`/api/v1/workflows/${selectedWorkflow.value}/runs`, {
      file_ids: fileIds.value,
      inputs: { message: message.value },
    })
    answer.value = data.answer
    message.value = ''
    fileIds.value = []
  } catch {
    error.value = '工作流执行失败，请稍后重试。'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section class="page chat-page">
    <header class="topbar"><div><p class="eyebrow">AI WORKSPACE</p><h1>今天需要处理什么？</h1><p class="muted">选择一个已授权的工作流，上传资料并直接描述你的目标。</p></div><el-tag type="success" effect="light">{{ portal.user.department }} · {{ portal.user.role === 'platform_admin' ? '管理员' : '员工' }}</el-tag></header>
    <div class="chat-layout">
      <div class="conversation-panel">
        <div v-if="!answer" class="empty-chat"><div class="empty-icon">✦</div><h2>让 AI 帮你完成一项工作</h2><p>例如：整理这份会议纪要，提取待办事项并按负责人分组。</p></div>
        <div v-else class="answer-card"><div class="answer-label">{{ activeWorkflow?.name }}</div><p>{{ answer }}</p><small>演示结果 · 后续接入真实模型和引用链</small></div>
        <div class="composer"><div class="composer-toolbar"><el-select v-model="selectedWorkflow" size="small" style="width: 210px" placeholder="选择工作流"><el-option v-for="workflow in portal.workflows" :key="workflow.workflow_id" :label="workflow.name" :value="workflow.workflow_id" /></el-select><el-button text @click="fileInput?.click()">添加文件</el-button><input ref="fileInput" hidden type="file" accept=".pdf,.doc,.docx,.xls,.xlsx,.txt,.jpg,.jpeg,.png" @change="uploadFile" /><span class="toolbar-hint">当前只运行你已获授权的工作流</span></div><div v-if="fileIds.length" class="file-hint">已添加 {{ fileIds.length }} 个文件</div><div v-if="error" class="error-banner">{{ error }}</div><div class="input-row"><el-input v-model="message" type="textarea" :rows="3" resize="none" placeholder="告诉工作流你需要什么，支持 PDF、Word、TXT 或图片" @keydown.enter.exact.prevent="sendMessage" /><el-button type="primary" :loading="sending" @click="sendMessage">发送</el-button></div></div>
      </div>
      <aside class="quick-panel"><p class="eyebrow">已授权工作流</p><div v-for="workflow in portal.workflows" :key="workflow.workflow_id" class="quick-agent" :class="{ active: selectedWorkflow === workflow.workflow_id }" @click="selectedWorkflow = workflow.workflow_id"><div class="agent-icon">{{ workflow.name.slice(0, 1) }}</div><div><strong>{{ workflow.name }}</strong><small>{{ workflow.category }}</small></div></div><div class="permission-note">权限由平台统一控制，页面只展示当前身份可使用的工作流。</div></aside>
    </div>
  </section>
</template>
