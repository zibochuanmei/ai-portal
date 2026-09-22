import { defineStore } from 'pinia'
import { api } from '../api/client'

export interface AgentSummary {
  id: string
  name: string
  description: string
  category: string
  status: 'ready' | 'draft'
  requires_knowledge_base: boolean
}

export const usePortalStore = defineStore('portal', {
  state: () => ({
    user: { display_name: '演示员工', department: '技术部', role: 'employee' },
    agents: [] as AgentSummary[],
    loading: false,
  }),
  actions: {
    async loadAgents() {
      this.loading = true
      try {
        const { data } = await api.get<AgentSummary[]>('/api/v1/agents')
        this.agents = data
      } finally {
        this.loading = false
      }
    },
  },
})
