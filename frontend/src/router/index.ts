import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../modules/chat/ChatView.vue'
import AgentsView from '../modules/agents/AgentsView.vue'
import AdminView from '../modules/admin/AdminView.vue'
import { usePortalStore } from '../stores/portal'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/chat' },
    { path: '/chat', component: ChatView },
    { path: '/agents', component: AgentsView },
    { path: '/admin', component: AdminView, meta: { requiresAdmin: true } },
  ],
})

router.beforeEach(async (to) => {
  if (!to.meta.requiresAdmin) return true
  const portal = usePortalStore()
  if (!portal.user.id) {
    try {
      await portal.loadCurrentUser()
    } catch {
      return '/chat'
    }
  }
  return portal.user.role === 'platform_admin' ? true : '/chat'
})

export default router
