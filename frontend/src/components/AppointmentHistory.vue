<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
 
const router = useRouter()
const token = localStorage.getItem('token')
const appointments = ref([])
 
onMounted(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/api/patient/appointment_history', {
            headers: { Authorization: `Bearer ${token}` }
        })
        appointments.value = response.data.data
    } catch (error) {
        console.error('Error fetching appointments:', error.response)
    }
})
</script>

<template>
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>My Appointment History</h1>
            </div>
            <br>
            <div class="header-actions">
                <a @click="router.push('/patient')" class="primary">Back to Dashboard</a>
            </div>
        </header>
 
        <div class="appoint">
            <h2>All Appointments</h2>
            <p v-if="appointments.length === 0">No appointments found.</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Doctor</th>
                        <th>Department</th>
                        <th>Mode</th>
                        <th>Status</th>
                        <th>Treatment</th>
                        <th>Prescription</th>
                        <th>Additional Info</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="appt in appointments" :key="appt.appointment_id">
                        <td>{{ appt.appointment_date }}</td>
                        <td>{{ appt.appointment_time }}</td>
                        <td>{{ appt.doctor_name }}</td>
                        <td>{{ appt.department }}</td>
                        <td>{{ appt.mode }}</td>
                        <td>{{ appt.status }}</td>
                        <td>{{ appt.treatment }}</td>
                        <td>{{ appt.prescription }}</td>
                        <td>{{ appt.info }}</td>
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
    flex-direction: column;
    justify-content: center;
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
