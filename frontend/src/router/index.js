import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AdminView from '@/views/AdminView.vue' 
import PatientView from '@/views/PatientView.vue'
import DoctorView from '@/views/DoctorView.vue'
import PatientReg from '@/components/PatientReg.vue';
import Login from '@/components/Login.vue';
import DepartInfo from '@/components/DepartInfo.vue';
import PatientInfo from '@/components/PatientInfo.vue';
import DoctorSlots from '@/components/DoctorSlots.vue';
import BookSlot from '@/components/BookSlot.vue';
import Treatment from '@/components/Treatment.vue';
import PatientHistory from '@/components/PatientHistory.vue';


const routes = [
  { path: '/', component: Home },
  { path: '/register', component: PatientReg },
  { path: '/login', component: Login },
  { path: '/admin', component: AdminView, meta: { requiresAuth: true, role: 'admin' }},
  { path: '/patient', component: PatientView, meta: { requiresAuth: true, role: 'patient' }},
  { path: '/doctor', component: DoctorView, meta: { requiresAuth: true, role: 'doctor' }},
  { path: '/department/:id', component: DepartInfo, meta: { requiresAuth: true }},
  { path: '/patient_info/:id', component: PatientInfo, meta: { requiresAuth: true, role: 'admin' }},
  { path: '/doctor/add_slots', component: DoctorSlots, meta: { requiresAuth: true, role: 'doctor' }},
  { path: '/book_slot/:doctor_id', component: BookSlot, meta: { requiresAuth: true, role: 'patient' }},
  { path: '/doctor/treatment/:appointment_id', component: Treatment, meta: { requiresAuth: true, role: 'doctor' }},
  { path: '/doctor/patient_history/:patient_id', component: PatientHistory, meta: { requiresAuth: true, role: 'doctor' }},
  { path: '/:catchAll(.*)', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router