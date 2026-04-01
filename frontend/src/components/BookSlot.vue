<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useRouter, useRoute } from 'vue-router'

const toast = useToast()
const router = useRouter()
const route = useRoute()
const token = localStorage.getItem('token')
const slots = ref({})
const doctorId = route.params.doctor_id
const noslots = ref(false)

const showSlots = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5001/api/patient/select_slot/${doctorId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        slots.value = response.data.data
    } catch (error) {
        if (error.response?.status == 404) {
            noslots.value = true
        } else if (error.response?.status == 400) {
            toast.error("Please complete your profile before booking an appointment.")
            router.push('/patient')
        } else {
            console.error("Error loading slots:", error)
        }
    }
}

const bookSlot = async (present_id) => {
    if (!confirm('Are you sure you want to book this slot?')) return
    try {
        await axios.put(`http://127.0.0.1:5001/api/patient/book_slot/${present_id}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Slot booked successfully!')
        showSlots()
    } catch (error) {
        toast.error('Could not book slot.')
        console.error('Error booking slot:', error.response)
    }
}

onMounted(() => {
    showSlots()
})

</script>

<template>
    <div>
        <button @click="router.go(-1)">Back</button>
        <h1>Available Slots</h1>
 
        <p v-if="noslots">No available slots yet.</p>
 
        <div v-else v-for="(daySlots, date) in slots" :key="date">
            <h3>{{ date }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Slot</th>
                        <th>Start</th>
                        <th>End</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="slot in daySlots" :key="slot.present_id">
                        <td>{{ slot.slot_number }}</td>
                        <td>{{ slot.start_time }}</td>
                        <td>{{ slot.end_time }}</td>
                        <td>
                            <button @click="bookSlot(slot.present_id)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>