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
        <div>
        <h1>Patient Details</h1>
        <div v-if="patient">
            <table>
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
        <p v-else>No patient details available.</p>
        <button @click="goBack">Back to Dashboard</button>
    </div>
    
</template>