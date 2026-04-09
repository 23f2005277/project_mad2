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
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>My Availability</h1>
            </div>
            <div class="header-actions">
                <a @click="router.push('/doctor')" class="primary">Back to Dashboard</a>
            </div>
        </header>
 
        <div v-for="(daySlots, date) in slots" :key="date" class="appoint">
            <h2>{{ date.split('-').reverse().join('-') }}</h2>
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
                                :class="slot.active ? 'secondary-ca' : 'secondary-c'"
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
 
.appoint button {
    display: inline-block;
    min-width: 100px;
    min-height: 30px;
    cursor: pointer;
    border-radius: 10px;
    padding: 10px 25px;
    border: none;
}
 
.appoint button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
 
.secondary-c {
    background-color: rgb(29, 144, 29);
    color: #f9f9f9;
    font-weight: 600;
}
 
.secondary-ca {
    background-color: rgb(226, 58, 58);
    color: #f9f9f9;
    font-weight: 600;
}
</style>
