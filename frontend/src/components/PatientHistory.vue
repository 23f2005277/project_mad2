<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
 
const route = useRoute()
const router = useRouter()
const token = localStorage.getItem('token')
 
const patientId = route.params.patient_id
const patientName = ref(null)
const patientAge = ref(null)
const patientMedicalHistory = ref(null)
const history = ref([])
 
onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5001/api/doctor/patient_history/${patientId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        patientName.value = response.data.patient_name
        patientAge.value = response.data.age
        patientMedicalHistory.value = response.data.medical_history
        history.value = response.data.data
    } catch (error) {
        console.error('Error loading patient history:', error.response)
    }
})
</script>

<template>
    <div>
        <button @click="router.push('/doctor')">Back to Dashboard</button>
 
        <h1>{{ patientName }}</h1>
        <p><strong>Medical History:</strong> {{ patientMedicalHistory || 'None recorded' }}</p>
        <p><strong>Age:</strong> {{ patientAge || 'None recorded' }}</p>

        <h2>Treatment History</h2>
        <p v-if="history.length === 0">No treatment history found.</p>
        <table v-else>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Treatment</th>
                    <th>Prescription</th>
                    <th>Additional Info</th>
                    <th>Visit Method</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="record in history" :key="record.treatment_id">
                    <td>{{ record.appointment_date }}</td>
                    <td>{{ record.doctor_name }}</td>
                    <td>{{ record.department }}</td>
                    <td>{{ record.treatment}}</td>
                    <td>{{ record.prescription }}</td>
                    <td>{{ record.info }}</td>
                    <td>{{ record.visit_method }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
 
