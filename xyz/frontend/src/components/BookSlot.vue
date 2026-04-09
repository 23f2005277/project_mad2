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
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>Available Slots</h1>
            </div>
            <br>
            <div class="header-actions">
                <a @click="router.go(-1)" class="primary">Back</a>
            </div>
        </header>
 
        <div class="appoint">
            <h2>Select a Slot</h2>
            <p v-if="noslots">No available slots yet.</p>
 
            <div v-else v-for="(daySlots, date) in slots" :key="date" class="day-block">
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
                                <button class="secondary-c" @click="bookSlot(slot.present_id)">Book</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
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
 
.day-block {
    margin-bottom: 25px;
}
 
.day-block h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: #333;
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
    min-width: 80px;
    min-height: 30px;
    cursor: pointer;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
}
 
.secondary-c {
    background-color: rgb(29, 144, 29);
    color: #f9f9f9;
    font-weight: 600;
}
</style>