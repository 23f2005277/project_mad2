<script setup>

import { reactive, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
 
const toast = useToast()
const token = localStorage.getItem('token')
const emit = defineEmits(['patientUpdated'])
 
const Patientform = reactive({
    email_id: '',
    password: '',
    name: '',
    age: '',
    gender: '',
    address: '',
    contact: '',
    medical_history: ''
})

onMounted(async () => {
    try {
        const response = await axios.get('http://localhost:5001/api/patient_details', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const data = response.data.data
        Patientform.username = data.username
        Patientform.email_id = data.email
        Patientform.name = data.name
        Patientform.age = data.age
        Patientform.gender = data.gender
        Patientform.address = data.address
        Patientform.contact = data.contact
        Patientform.medical_history = data.medical_history
    } catch (error) {
        console.error('Error in getting patient details:', error)
    }
})

const updatePatient = async () => {
    try {
        await axios.put('http://localhost:5001/api/update_patient', Patientform, {
            headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Patient details updated successfully!')
        emit('patientUpdated')
    } catch (error) {
        toast.error('Failed to update patient details.')
        console.error('Error while updating patient:', error)
    }
}
</script>

<template>
    <div class="list">
        <h2>Edit Profile</h2>
        <form @submit.prevent="updatePatient" class="form-body">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="Patientform.username" disabled />
            </div>
            <div class="form-group">
                <label for="email_id">Email:</label>
                <input type="email" id="email_id" v-model="Patientform.email_id" required />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="Patientform.password" placeholder="Leave blank to keep current password" />
            </div>
            <div class="form-group">
                <label for="name">Full Name:</label>
                <input type="text" id="name" v-model="Patientform.name" required />
            </div>
            <div class="form-group">
                <label for="age">Age:</label>
                <input type="number" id="age" v-model="Patientform.age" min="0" required />
            </div>
            <div class="form-group">
                <label for="gender">Gender:</label>
                <select id="gender" v-model="Patientform.gender" required>
                    <option value="" disabled>Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                </select>
            </div>
            <div class="form-group">
                <label for="address">Address:</label>
                <textarea id="address" v-model="Patientform.address" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label for="contact">Contact:</label>
                <input type="text" id="contact" v-model="Patientform.contact" required />
            </div>
            <div class="form-group">
                <label for="medical_history">Medical History:</label>
                <textarea id="medical_history" v-model="Patientform.medical_history" rows="3"></textarea>
            </div>
            <div class="form-actions">
                <button type="submit">Update Profile</button>
            </div>
        </form>
    </div>
</template>
 
<style scoped>
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
 
.form-body {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
 
.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
 
.form-group label {
    font-weight: 500;
    font-size: 15px;
}
 
.form-group input,
.form-group textarea,
.form-group select {
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
}
 
.form-group input:disabled {
    background-color: #e9e9e9;
    color: #888;
    cursor: not-allowed;
}
 
.form-actions {
    display: flex;
    gap: 10px;
}
 
.form-actions button {
    background-color: #007bff;
    color: white;
    cursor: pointer;
    font-size: 14px;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
}

</style>