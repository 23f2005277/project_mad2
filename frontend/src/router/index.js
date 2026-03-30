import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AdminView from '@/views/AdminView.vue' 
import PatientView from '@/views/PatientView.vue'
import DoctorView from '@/views/DoctorView.vue'
import PatientReg from '@/components/PatientReg.vue';
import Login from '@/components/Login.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/register', component: PatientReg },
  { path: '/login', component: Login },
  { path: '/admin', component: AdminView }, 
  { path: '/patient', component: PatientView },
  { path: '/doctor', component: DoctorView },
  { path: '/:catchAll(.*)', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router