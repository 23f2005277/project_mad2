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
        const response = await axios.get(`http://127.0.0.1:5001/api/admin/treatment_info/${patientId}`, {
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
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>{{ patientName }}</h1>
                <p>Treatment History</p>
            </div>
            <div class="header-actions">
                <a @click="router.push('/admin')" class="primary">Back to Dashboard</a>
            </div>
        </header>
 
        <div class="list">
            <h2>Patient Details</h2>
            <table>
                <tbody>
                    <tr>
                        <th>Age</th>
                        <td>{{ patientAge || 'None recorded' }}</td>
                    </tr>
                    <tr>
                        <th>Medical History</th>
                        <td>{{ patientMedicalHistory || 'None recorded' }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
 
        <div class="appoint">
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
                        <td>{{ record.treatment }}</td>
                        <td>{{ record.prescription }}</td>
                        <td>{{ record.info }}</td>
                        <td>{{ record.visit_method }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
 
    </div>
</template>
 
<style scoped>
* {
    margin: 0px;
    padding: 0px;
}
 
.page-wrapper {
    background-color: rgb(133, 133, 218);
    min-height: 100vh;
    padding: 20px;
}
 
header {
    text-align: center;
    margin: 5vh;
    height: 20vh;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: wrap;
    background-color: #f9f9f9;
    border-radius: 15px;
}
 
.header-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}
 
.primary {
    padding: 15px 25px;
    border: none;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 900;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    background: rgb(89, 89, 220);
    color: #f9f9f9;
}
 
.list {
    margin-bottom: 40px;
    padding: 25px;
    background-color: #f9f9f9;
    border-radius: 8px;
}
 
.list h2 {
    margin-bottom: 20px;
    color: black;
    font-size: 25px;
    border-bottom: 2px solid black;
    padding-bottom: 10px;
}
 
.list table {
    width: 100%;
    border-collapse: collapse;
    background-color: #f9f9f9;
}
 
.list table th {
    background-color: #2468b0;
    color: white;
    padding: 15px;
    text-align: left;
    font-weight: 500;
    font-size: 16px;
    width: 200px;
}
 
.list table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
    font-size: 14px;
}
 
.appoint {
    margin-bottom: 40px;
    padding: 25px;
    background-color: #f9f9f9;
    border-radius: 8px;
}
 
.appoint h2 {
    margin-bottom: 20px;
    color: black;
    font-size: 25px;
    border-bottom: 2px solid black;
    padding-bottom: 10px;
}
 
.appoint table {
    width: 100%;
    border-collapse: collapse;
    background-color: #f9f9f9;
}
 
.appoint th {
    background-color: #2468b0;
    color: white;
    padding: 15px;
    text-align: left;
    font-weight: 500;
    font-size: 16px;
}
 
.appoint td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
    font-size: 14px;
}
</style>
