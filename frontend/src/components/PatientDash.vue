<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import PatientDetails from "./PatientDetails.vue";


const router = useRouter();
const toast = useToast();
const username = localStorage.getItem("username");
const token = localStorage.getItem("token");

const departments = ref([]);
const showPatientForm = ref(false);
const appointments = ref([])

const showAllAppointments = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/patient/allappointments', {
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
    await axios.delete(`http://127.0.0.1:5001/api/patient/cancel_appointment/${appointmentId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    toast.success('Appointment cancelled successfully!');
    showAllAppointments();
  } catch (error) {
    toast.error('Could not cancel appointment.')
    console.error('Error in cancelling appointment:', error.response);
  }
}

onMounted(async () => {
  try {
    const response = await axios.get(
      "http://localhost:5001/api/alldepartments",
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    departments.value = response.data.data;
  } catch (error) {
    console.error("Error fetching departments:", error);
  }
});

const togglePatientForm = () => {
  showPatientForm.value = !showPatientForm.value;
};

const onPatientUpdated = () => {
  showPatientForm.value = false;
}

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  router.push("/login");
};

onMounted(() => {
  showAllAppointments()
})

</script>

<template>
  <div>
    <h1>Welcome, {{ username }}!</h1>
    <p>You are logged in as a Patient.</p>
    <button @click="logout()">Logout</button>
    <button @click="togglePatientForm"> {{ showPatientForm ? 'Hide' : 'Update Profile' }}</button>
    <PatientDetails v-if="showPatientForm" @patientUpdated="onPatientUpdated" />

    <h2>Departments</h2>
    <table>
      <thead>
        <tr>
          <th>Department Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dept in departments" :key="dept.department_id">
          <td>{{ dept.department_name }}</td>
          <td> 
            <RouterLink :to="`/department/${dept.department_id}`">
              <button>View Details</button>
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
        <h2>Appointments</h2>
    <p v-if="appointments.length === 0">No appointments found.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Doctor Name</th>
          <th>Department</th>
          <th>Appointment Date</th>
          <th>Appointment Time</th>
          <th>Mode</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appointment in appointments" :key="appointment.appointment_id">
          <td>{{ appointment.doctor_name }}</td>
          <td>{{ appointment.department_name }}</td>
          <td>{{ appointment.appointment_date }}</td>
          <td>{{ appointment.appointment_time }}</td>
          <td>{{ appointment.mode }}</td>
          <td>
            <button @click="cancelAppointment(appointment.appointment_id)">Cancel</button>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>
