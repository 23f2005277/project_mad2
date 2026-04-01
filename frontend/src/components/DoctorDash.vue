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
  <div>
    <h1>Welcome, {{ username }}!</h1>
    <p>You are logged in as a Doctor.</p>
    <button @click="logout()">Logout</button>
    <RouterLink to="/doctor/add_slots">
      <button>Add Available Slots</button>
    </RouterLink>

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
              <button>{{ appointment.has_treatment ? 'Update Treatment' : 'Add Treatment' }}</button>
            </RouterLink>
            <button v-if="appointment.has_treatment && appointment.status === 'Booked'"
              @click="completeAppointment(appointment.appointment_id)">
              Mark Complete
            </button>
            <button 
              v-if="appointment.status === 'Booked'"
              @click="cancelAppointment(appointment.appointment_id)">
              Cancel
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h2>My Patients</h2>
<p v-if="patients.length === 0">No patients yet.</p>
<table v-else>
    <tbody>
        <tr v-for="patient in patients" :key="patient.patient_id">
            <td>{{ patient.name }}</td>
            <td>
                <RouterLink :to="`/doctor/patient_history/${patient.patient_id}`" >
                    <button>View History</button>
                </RouterLink>
            </td>
        </tr>
    </tbody>
</table>
  </div>
</template>