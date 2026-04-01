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
    <div>
        <button @click="router.push('/doctor')">Back to Dashboard</button>
        <h1>{{ existingTreatment ? 'Update Treatment' : 'Add Treatment' }}</h1>
 
        <form @submit.prevent="addTreatment">
            <div>
                <label for="treatment">Treatment:</label>
                <textarea id="treatment" v-model="treatmentData.treatment" rows="3" required></textarea>
            </div>
            <div>
                <label for="prescription">Prescription:</label>
                <textarea id="prescription" v-model="treatmentData.prescription" rows="3" required></textarea>
            </div>
            <div>
                <label for="info">Additional Info:</label>
                <textarea id="info" v-model="treatmentData.info" rows="3"></textarea>
            </div>
            <div>
                <label for="visit_method">Visit Method:</label>
                <select id="visit_method" v-model="treatmentData.visit_method">
                    <option value="" disabled>Select visit method</option>
                    <option value="In-person">In-person</option>
                    <option value="Online">Online</option>
                </select>
            </div>
            <button type="submit">Save Treatment</button>
        </form>
    </div>
</template>