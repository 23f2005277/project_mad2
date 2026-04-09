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
const appointments = ref([]);

const searchQuery = ref("");
const searchResults = ref([]);
const searchPerformed = ref(false);

const showAllAppointments = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:5001/api/patient/allappointments",
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    appointments.value = response.data.data;
  } catch (error) {
    console.error("Error in loading appointments:", error.response);
  }
};

const cancelAppointment = async (appointmentId) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  try {
    await axios.delete(
      `http://127.0.0.1:5001/api/patient/cancel_appointment/${appointmentId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    toast.success("Appointment cancelled successfully!");
    showAllAppointments();
  } catch (error) {
    toast.error("Could not cancel appointment.");
    console.error("Error in cancelling appointment:", error.response);
  }
};

const searchDoctors = async () => {
  if (!searchQuery.value.trim()) return;
  searchPerformed.value = false;

  try {
    const response = await axios.get(
      "http://127.0.0.1:5001/api/patient/search",
      {
        headers: { Authorization: `Bearer ${token}` },
        params: { q: searchQuery.value },
      },
    );
    searchResults.value = response.data.data;
    searchPerformed.value = true;
  } catch (error) {
    toast.error("Search failed.");
    console.error("Search error:", error.response);
  }
};

const clearSearch = () => {
  searchQuery.value = "";
  searchResults.value = [];
  searchPerformed.value = false;
};

const togglePatientForm = () => {
  showPatientForm.value = !showPatientForm.value;
};

const onPatientUpdated = () => {
  showPatientForm.value = false;
};

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  router.push("/");
};

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
  showAllAppointments();
});
</script>

<template>
  <div class="page-wrapper">

    <header>
      <div>
        <h1>Welcome, {{ username }}!</h1>
        <p>You are logged in as a Patient.👨</p>
      </div>
      <div class="header-actions">
        <a @click="togglePatientForm" class="primary">
          {{ showPatientForm ? "Hide" : "Update Profile" }}
        </a>
        <RouterLink to="/patient/appointment_history" class="primary">My Medical History</RouterLink>
        <a @click="logout" class="primary">Logout🔒</a>
      </div>
    </header>
 
    <PatientDetails v-if="showPatientForm" @patientUpdated="onPatientUpdated" />

    <div class="appoint">
      <h2>Search Doctors🔎</h2>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name, qualification, or department..."
        />
        <button class="secondary-p" @click="searchDoctors">Search</button>
        <button class="secondary-ca" @click="clearSearch">Clear</button>
      </div>
 
      <div v-if="searchPerformed">
        <p v-if="searchResults.length === 0">No doctors found.</p>
        <table v-else>
          <thead>
            <tr>
              <th>Name</th>
              <th>Qualification</th>
              <th>Department</th>
              <th>Experience (yrs)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in searchResults" :key="doc.doctor_id">
              <td>{{ doc.name }}</td>
              <td>{{ doc.qualification }}</td>
              <td>{{ doc.department }}</td>
              <td>{{ doc.experience_years }}</td>
              <td>
                <RouterLink :to="`/department/${doc.department_id}`">
                  <button class="secondary-p">Book Appointment</button>
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
 
    <div class="depart">
      <h2>Departments</h2>
      <table>
        <thead>
          <tr>
            <th>Department Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dept in departments" :key="dept.department_id">
            <td>{{ dept.department_name }}</td>
            <td>
              <RouterLink :to="`/department/${dept.department_id}`">
                <button class="secondary-p">View Details</button>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="appoint">
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
              <button
                v-if="appointment.status === 'Booked'"
                class="secondary-ca"
                @click="cancelAppointment(appointment.appointment_id)"
              >
                Cancel
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
  min-width: 100px;
  min-height: 30px;
  cursor: pointer;
  border-radius: 10px;
  padding: 10px 25px;
  border: none;
}
 
.search-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
 
.search-bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
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
