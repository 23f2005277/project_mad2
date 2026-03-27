import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AdminView from '@/views/AdminView.vue' 
import PatientView from '@/views/PatientView.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/admin', component: AdminView }, 
  { path: '/patient', component: PatientView },
  { path: '/:catchAll(.*)', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router