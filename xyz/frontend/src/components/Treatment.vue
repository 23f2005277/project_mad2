<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
 
const route = useRoute()
const router = useRouter()
const toast = useToast()
const token = localStorage.getItem('token')

const appointmentId = route.params.appointment_id
const existingTreatment = ref(null)

const treatmentData = reactive({
  treatment: '',
  prescription: '',
  info: '',
  visit_method: ''
})

onMounted(async () => {
     try {
        const response = await axios.get(`http://127.0.0.1:5001/api/doctor/treatment/${appointmentId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        const data = response.data.data
        if (data) {
            existingTreatment.value = data
            treatmentData.treatment = data.treatment
            treatmentData.prescription = data.prescription
            treatmentData.info = data.info
            treatmentData.visit_method = data.visit_method
        }
     } catch (error) {
        console.error('Error in loading treatment details:', error.response)
     }
})


const addTreatment = async () => {
    try {
        await axios.put(`http://127.0.0.1:5001/api/doctor/update_treatment/${appointmentId}`, treatmentData, {
            headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Treatment saved successfully!')
        existingTreatment.value = { ...treatmentData }
        router.push('/doctor')
    } catch (error) {
        toast.error('Could not save treatment.')
        console.error('Error saving treatment:', error.response)
    }
}

</script>

<template>
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>{{ existingTreatment ? 'Update Treatment' : 'Add Treatment' }}</h1>
            </div>
            <div class="header-actions">
                <a @click="router.push('/doctor')" class="primary">Back to Dashboard</a>
            </div>
        </header>
 
        <div class="list">
            <h2>Treatment Details</h2>
            <form @submit.prevent="addTreatment" class="form-body">
                <div class="form-group">
                    <label for="treatment">Treatment:</label>
                    <textarea id="treatment" v-model="treatmentData.treatment" rows="3" required></textarea>
                </div>
                <div class="form-group">
                    <label for="prescription">Prescription:</label>
                    <textarea id="prescription" v-model="treatmentData.prescription" rows="3" required></textarea>
                </div>
                <div class="form-group">
                    <label for="info">Additional Info:</label>
                    <textarea id="info" v-model="treatmentData.info" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="visit_method">Visit Method:</label>
                    <select id="visit_method" v-model="treatmentData.visit_method">
                        <option value="" disabled>Select visit method</option>
                        <option value="In-person">In-person</option>
                        <option value="Online">Online</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="submit">Save Treatment</button>
                </div>
            </form>
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
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
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
 
.form-group textarea,
.form-group select {
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
    resize: vertical;
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
 