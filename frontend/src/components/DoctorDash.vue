<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const username = localStorage.getItem('username')
const token = localStorage.getItem('token')
const router = useRouter()
const toast = useToast()

const appointments = ref([])
const patients = ref([])

const showAllAppointments = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/doctor/allappointments', {
      headers: { Authorization: `Bearer ${token}` }
    });
    appointments.value = response.data.data;
  } catch (error) {
    console.error('Error in loading appointments:', error.response);
  }
}

const cancelAppointment = async (appointmentId) => {
  if (!confirm('Are you sure you want to cancel this appointment?')) return
  try {
    await axios.delete(`http://127.0.0.1:5001/api/doctor/cancel_appointment/${appointmentId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    toast.success('Appointment cancelled successfully!');
    showAllAppointments();
  } catch (error) {
    toast.error('Could not cancel appointment.')
    console.error('Error in cancelling appointment:', error.response);
  }
}

const completeAppointment = async (appointmentId) => {
  if (!confirm('Are you sure you want to mark this appointment as complete?')) return
  try {
    await axios.put(`http://127.0.0.1:5001/api/doctor/complete_appointment/${appointmentId}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    toast.success('Appointment marked as complete!');
    showAllAppointments();
  } catch (error) {
    toast.error('Could not complete appointment.')
    console.error('Error completing appointment:', error.response);
  }
}

const showPatients = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/api/doctor/mypatients', {
            headers: { Authorization: `Bearer ${token}` }
        })
        patients.value = response.data.data
    } catch (error) {
        console.error('Error in loading patients:', error.response)
    }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/')
}

onMounted(() => {
  showAllAppointments();
  showPatients();
})
</script>

<template>
  <div class="page-wrapper">
    <header>
      <div>
        <h1>Welcome, {{ username }}!</h1>
        <p>You are logged in as a Doctor.</p>
      </div>
      <div class="header-actions">
        <RouterLink to="/doctor/add_slots" class="primary">Add Available Slots</RouterLink>
        <a @click="logout" class="primary">Logout</a>
      </div>
    </header>
 
    <div class="appoint">
      <h2>Appointments</h2>
      <p v-if="appointments.length === 0">No appointments found.</p>
      <table v-else>
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Appointment Date</th>
            <th>Appointment Time</th>
            <th>Mode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appointment in appointments" :key="appointment.appointment_id">
            <td>{{ appointment.patient_name }}</td>
            <td>{{ appointment.appointment_date }}</td>
            <td>{{ appointment.appointment_time }}</td>
            <td>{{ appointment.mode }}</td>
            <td>
              <RouterLink :to="`/doctor/treatment/${appointment.appointment_id}`">
                <button class="secondary-p">
                  {{ appointment.has_treatment ? 'Update Treatment' : 'Add Treatment' }}
                </button>
              </RouterLink>
              <button
                v-if="appointment.has_treatment && appointment.status === 'Booked'"
                class="secondary-c"
                @click="completeAppointment(appointment.appointment_id)">
                Mark Complete
              </button>
              <button
                v-if="appointment.status === 'Booked'"
                class="secondary-ca"
                @click="cancelAppointment(appointment.appointment_id)">
                Cancel
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
 
    <div class="depart">
      <h2>My Patients</h2>
      <p v-if="patients.length === 0">No patients yet.</p>
      <table v-else>
        <tbody>
          <tr v-for="patient in patients" :key="patient.patient_id">
            <td>{{ patient.name }}</td>
            <td>
              <RouterLink :to="`/doctor/patient_history/${patient.patient_id}`">
                <button class="secondary-p">View History</button>
              </RouterLink>
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
 
.appoint,
.depart {
  margin-bottom: 40px;
  padding: 25px;
  background-color: #f9f9f9;
  border-radius: 8px;
}
 
.appoint table,
.depart table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9;
}
 
.appoint h2,
.depart h2 {
  margin-bottom: 20px;
  color: black;
  font-size: 25px;
  border-bottom: 2px solid black;
  padding-bottom: 10px;
}
 
.appoint th {
  background-color: #2468b0;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 500;
  font-size: 16px;
}
 
.appoint td,
.depart td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
}
 
.appoint button {
  display: inline-block;
  justify-content: center;
  min-width: 100px;
  min-height: 30px;
  cursor: pointer;
  border-radius: 10px;
  padding: 10px 25px;
  border: none;
}
 
.secondary-p {
  background-color: rgb(89, 89, 220);
  color: #f9f9f9;
  font-weight: 600;
  margin-bottom: 5px;
}
 
.secondary-c {
  background-color: rgb(29, 144, 29);
  color: #f9f9f9;
  font-weight: 600;
  margin-top: 2px;
  margin-bottom: 5px;
}
 
.secondary-ca {
  background-color: rgb(226, 58, 58);
  color: #f9f9f9;
  font-weight: 600;
  margin-bottom: 2px;
}
</style>