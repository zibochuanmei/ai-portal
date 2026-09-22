import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../modules/chat/ChatView.vue'
import AgentsView from '../modules/agents/AgentsView.vue'
import AdminView from '../modules/admin/AdminView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/chat' },
    { path: '/chat', component: ChatView },
    { path: '/agents', component: AgentsView },
    { path: '/admin', component: AdminView },
  ],
})
