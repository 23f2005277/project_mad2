<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'

const toast = useToast()
const router = useRouter()
const token = localStorage.getItem('token')
const slots = ref({})

const showSlots = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/api/doctor/add_slots', {
            headers: { Authorization: `Bearer ${token}` }
        })
        slots.value = response.data.data
    } catch (error) {
        console.error("Error loading slots:", error)
    }
}

const toggleSlot = async (present_id) => {
    try {
        await axios.put(`http://127.0.0.1:5001/api/doctor/add_slots/${present_id}/toggle`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        showSlots()
    } catch (error) {
        console.error("Error toggling slot:", error)
        toast.error("Failed to update slot status.")
    }
}

onMounted(() => {
    showSlots()
})

</script>

<template>
       <div>
        <button @click="router.push('/doctor')">go Back</button>
        <h1>My Availability</h1>
        <div v-for="(daySlots, date) in slots" :key="date">
            <h3>{{ date.split('-').reverse().join('-') }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Slot</th>
                        <th>Start</th>
                        <th>End</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="slot in daySlots" :key="slot.present_id">
                        <td>{{ slot.slot_number }}</td>
                        <td>{{ slot.start_time }}</td>
                        <td>{{ slot.end_time }}</td>
                        <td>{{ slot.booked ? 'Booked' : slot.active ? 'Available' : 'Inactive' }}</td>
                        <td>
                            <button 
                                @click="toggleSlot(slot.present_id)" 
                                :disabled="slot.booked">
                                {{ slot.active ? 'Deactivate' : 'Activate' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template> 
