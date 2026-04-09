<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
 
const route = useRoute()
const router = useRouter()
const token = localStorage.getItem('token')

const patient = ref(null)
const patientId = route.params.id

const goBack = () => {
    router.push('/admin')
}

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5001/api/patient_info/${patientId}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        patient.value = response.data.data;
    } catch (error) {
        console.error('Error in loading patient details:', error.response);
    }
});

</script>

<template>
    <div class="page-wrapper">

        <header>
            <div>
                <h1>Patient Details</h1>
                <p v-if="patient">{{ patient.name }}</p>
            </div>
            <div class="header-actions">
                <a @click="goBack" class="primary">Back to Dashboard</a>
            </div>
        </header>

        <div class="list">
            <h2>Patient Information</h2>
            <p v-if="!patient">No patient details available.</p>
            <table v-else>
                <tbody>
                    <tr>
                        <th>Username</th>
                        <td>{{ patient.username }}</td>
                    </tr>
                    <tr>
                        <th>Email</th>
                        <td>{{ patient.email }}</td>
                    </tr>
                    <tr>
                        <th>Name</th>
                        <td>{{ patient.name }}</td>
                    </tr>
                    <tr>
                        <th>Age</th>
                        <td>{{ patient.age }}</td>
                    </tr>
                    <tr>
                        <th>Gender</th>
                        <td>{{ patient.gender }}</td>
                    </tr>
                    <tr>
                        <th>Address</th>
                        <td>{{ patient.address }}</td>
                    </tr>
                    <tr>
                        <th>Contact</th>
                        <td>{{ patient.contact }}</td>
                    </tr>
                    <tr>
                        <th>Medical History</th>
                        <td>{{ patient.medical_history }}</td>
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
 
table {
    width: 100%;
    border-collapse: collapse;
    background-color: #f9f9f9;
}
 
table th {
    background-color: #2468b0;
    color: white;
    padding: 15px;
    text-align: left;
    font-weight: 500;
    font-size: 16px;
    width: 200px;
}
 
table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
    font-size: 14px;
}
</style>