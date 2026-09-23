import { defineStore } from 'pinia'
import { api } from '../api/client'

export interface WorkflowSummary {
  workflow_id: string
  name: string
  description: string
  category: string
  status: 'ready' | 'draft'
  requires_knowledge_base: boolean
  can_run: boolean
}

export interface UserContext {
  id: string
  display_name: string
  department: string
  role: 'employee' | 'platform_admin'
}

export const usePortalStore = defineStore('portal', {
  state: () => ({
    user: { id: '', display_name: '加载中', department: '', role: 'employee' } as UserContext,
    workflows: [] as WorkflowSummary[],
    loading: false,
    error: '',
  }),
  actions: {
    async loadCurrentUser() {
      const { data } = await api.get<UserContext>('/api/v1/me')
      this.user = data
    },
    async loadWorkflows() {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.get<WorkflowSummary[]>('/api/v1/workflows')
        this.workflows = data
      } catch {
        this.error = '暂时无法加载工作流，请检查后端服务。'
      } finally {
        this.loading = false
      }
    },
  },
})
