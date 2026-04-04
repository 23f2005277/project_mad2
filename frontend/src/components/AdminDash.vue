<script setup>
import { ref, onMounted} from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification';
import AddDepartment from './AddDepartment.vue'
import AddDoctor from './AddDoctor.vue'
import UpdateDoc from './UpdateDoc.vue'
import UpdateDpt from './UpdateDpt.vue'

const router = useRouter()
const toast = useToast();
const username = localStorage.getItem('username')
const token = localStorage.getItem('token')


const docForm = ref(false)
const doctors = ref([])

const departForm = ref(false)
const departments = ref([])
const patients = ref([])
const Appointments = ref([])

const thisDoctor = ref(null)
const thisDpt = ref(null)

const searchQuery = ref('')
const searchType = ref('doctor')
const searchResults = ref([])
const searchPerformed = ref(false)

const toggleDocForm = () => {
  docForm.value = !docForm.value
}

const toggleDepartForm = () => {
  departForm.value = !departForm.value
}

const showAddDoctorForm = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/alldoctors', {
      headers: { Authorization: `Bearer ${token}` }
    });
    doctors.value = response.data.data;
  } catch (error) {
    console.error('Error in loading doctors:', error.response);
  }
}

const showAddDepartmentForm = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/alldepartments', {
      headers: { Authorization: `Bearer ${token}` }
    });
    departments.value = response.data.data;
  } catch (error) {
    console.error('Error in loading departments:', error.response);
  }
}

const showAllPatients = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/allpatients', {
      headers: { Authorization: `Bearer ${token}` }
    });
    patients.value = response.data.data;
  } catch (error) {
    console.error('Error in loading patients:', error.response);
  }
}

const showAllAppointments = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/admin/allappointment', {
      headers: { Authorization: `Bearer ${token}` }
    });
    Appointments.value = response.data.data;
  } catch (error) {
    console.error('Error in loading appointments:', error.response);
  }
}

const deleteDoctor = async (doctor_id) => {
  if (!confirm('Are you sure you want to delete this doctor?')) return

  try {
    await axios.delete(`http://127.0.0.1:5001/api/delete_doctor/${doctor_id}`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Doctor deleted successfully!') 
    showAddDoctorForm()
  } catch (error) {
    toast.error('Could not delete doctor.')
    console.error('Error in deleting doctor:', error.response);
  }
}

const deleteDepartment = async (department_id) => {
  if (!confirm('Are you sure you want to delete this department?')) return

  try {
    await axios.delete(`http://127.0.0.1:5001/api/delete_department/${department_id}`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Department deleted successfully!')
    showAddDepartmentForm()
  } catch (error) {
    toast.error('Could not delete department.')
    console.error('Error in deleting department:', error.response);
  }
}

const deletePatient = async (patient_id) => {
  if (!confirm('Are you sure you want to delete this patient?')) return
  try {
    await axios.delete(`http://127.0.0.1:5001/api/delete_patient/${patient_id}`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Patient deleted successfully!')
    showAllPatients()
  } catch (error) {
    toast.error('Could not delete patient.')
    console.error('Error in deleting patient:', error.response);
  }
}

const search = async () => {
  if (!searchQuery.value.trim()) return
  searchPerformed.value = false

  try {
    const response = await axios.get('http://127.0.0.1:5001/api/admin/search', {
      headers: { Authorization: `Bearer ${token}` },
      params: { q: searchQuery.value, type: searchType.value }
    })
    searchResults.value = response.data.data
    searchPerformed.value = true
  } catch (error) {
    toast.error('Search failed.')
    console.error('Search error:', error.response)
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  searchPerformed.value = false
}

const onDoctorAdded = () => {
  showAddDoctorForm()
  docForm.value = false
}

const onDoctorUpdated = () => {
  showAddDoctorForm()
  thisDoctor.value = null
}

const onDepartmentAdded = () => {
  showAddDepartmentForm()
  departForm.value = false
}

const onDepartmentUpdated = () => {
  showAddDepartmentForm()
  thisDpt.value = null
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/')
}

onMounted(() => {
  showAddDoctorForm();
  showAddDepartmentForm();
  showAllPatients();
  showAllAppointments();
})

</script>

<template>
  <div class="page-wrapper">

    <header>
      <div>
        <h1>Welcome, {{ username }}!</h1>
        <p>You are logged in as an Admin.</p>
      </div>
      <div class="header-actions">
        <div class="links">
          <span>Doctors: {{ doctors.length }}</span>
          <span>Patients: {{ patients.length }}</span>
          <span>Appointments: {{ Appointments.length }}</span>
        </div>
        <div class="links">
          <a @click="toggleDocForm">{{ docForm ? 'Hide' : 'Add Doctor' }}</a>
          <a @click="toggleDepartForm">{{ departForm ? 'Hide' : 'Add Department' }}</a>
          <a @click="logout">Logout</a>
        </div>
      </div>
    </header>
 
    <AddDoctor v-if="docForm" @doctorAdded="onDoctorAdded" />
    <AddDepartment v-if="departForm" @departmentAdded="onDepartmentAdded" />
    <UpdateDoc v-if="thisDoctor" :doctor="thisDoctor" @doctorUpdated="onDoctorUpdated" @cancelEdit="thisDoctor = null" />
    <UpdateDpt v-if="thisDpt" :department="thisDpt" @departmentUpdated="onDepartmentUpdated" @cancelEdit="thisDpt = null" />

    <div class="list">
      <h2>Search</h2>
      <div class="search-bar">
        <select v-model="searchType">
          <option value="doctor">Doctor</option>
          <option value="patient">Patient</option>
        </select>
        <input v-model="searchQuery" type="text" placeholder="Search by name, contact, email..." />
        <button @click="search">Search</button>
        <button @click="clearSearch">Clear</button>
      </div>
 
      <div v-if="searchPerformed">
        <p v-if="searchResults.length === 0">No results found.</p>
 
        <table v-else-if="searchType === 'doctor'">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Qualification</th>
              <th>Contact</th>
              <th>Department</th>
              <th>Experience (yrs)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in searchResults" :key="doc.doctor_id">
              <td>{{ doc.name }}</td>
              <td>{{ doc.email }}</td>
              <td>{{ doc.qualification }}</td>
              <td>{{ doc.contact }}</td>
              <td>{{ doc.department }}</td>
              <td>{{ doc.experience_years }}</td>
            </tr>
          </tbody>
        </table>
 
        <table v-else-if="searchType === 'patient'">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Gender</th>
              <th>Contact</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pat in searchResults" :key="pat.patient_id">
              <td>{{ pat.patient_id }}</td>
              <td>{{ pat.name }}</td>
              <td>{{ pat.gender }}</td>
              <td>{{ pat.contact }}</td>
              <td>
                <RouterLink :to="`/patient_info/${pat.patient_id}`">
                  <button>View</button>
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
 
    <div class="doctors-departments-container">
      <div class="list doctors">
        <h2>Doctors</h2>
        <p v-if="doctors.length === 0">No doctors added yet.</p>
        <table v-else>
          <thead>
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Qualification</th>
              <th>Exp (yrs)</th>
              <th>Contact</th>
              <th>Department</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doctor in doctors" :key="doctor.doctor_id">
              <td>{{ doctor.name }}</td>
              <td>{{ doctor.username }}</td>
              <td>{{ doctor.email }}</td>
              <td>{{ doctor.qualification }}</td>
              <td>{{ doctor.experience_years }}</td>
              <td>{{ doctor.contact }}</td>
              <td>{{ doctor.department }}</td>
              <td>
                <button @click="thisDoctor = doctor">Edit</button>
                <button @click="deleteDoctor(doctor.doctor_id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
 
      <div class="list departments">
        <h2>Departments</h2>
        <p v-if="departments.length === 0">No departments added yet.</p>
        <table v-else>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="department in departments" :key="department.department_id">
              <td>{{ department.department_name }}</td>
              <td>{{ department.department_description }}</td>
              <td>
                <button @click="thisDpt = department">Edit</button>
                <button @click="deleteDepartment(department.department_id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="appointments-container">
      <div class="list">
        <h2>Patients</h2>
        <p v-if="patients.length === 0">No patients registered yet.</p>
        <table v-else>
          <thead>
            <tr>
              <th>Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in patients" :key="patient.patient_id">
              <td>{{ patient.name }}</td>
              <td>
                <RouterLink :to="`/patient_info/${patient.patient_id}`">
                  <button>View</button>
                </RouterLink>
                <button @click="deletePatient(patient.patient_id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
 
      <div class="list">
        <h2>Upcoming Appointments</h2>
        <p v-if="Appointments.filter(a => a.status === 'Booked').length === 0">No upcoming appointments.</p>
        <table v-else>
          <thead>
            <tr>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Department</th>
              <th>Date</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in Appointments.filter(a => a.status === 'Booked')" :key="appointment.appointment_id">
              <td>{{ appointment.patient_name }}</td>
              <td>{{ appointment.doctor_name }}</td>
              <td>{{ appointment.department_name }}</td>
              <td>{{ appointment.appointment_date }}</td>
              <td>{{ appointment.appointment_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
 
    <div class="list">
      <h2>Past Appointments</h2>
      <p v-if="Appointments.filter(a => a.status === 'Completed').length === 0">No past appointments.</p>
      <table v-else>
        <thead>
          <tr>
            <th>Patient</th>
            <th>Doctor</th>
            <th>Department</th>
            <th>Date</th>
            <th>Time</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="appointment in Appointments.filter(a => a.status === 'Completed')" :key="appointment.appointment_id">
            <td>{{ appointment.patient_name }}</td>
            <td>{{ appointment.doctor_name }}</td>
            <td>{{ appointment.department_name }}</td>
            <td>{{ appointment.appointment_date }}</td>
            <td>{{ appointment.appointment_time }}</td>
            <td>
              <RouterLink :to="`/admin/treatment_info/${appointment.patient_id}`">
                <button>View</button>
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
  flex-direction: column;
  gap: 15px;
  font-size: 18px;
  margin-top: 15px;
}
 
.links {
  display: flex;
  justify-content: center;
  gap: 30px;
}
 
.header-actions a {
  text-decoration: none;
  background: rgb(89, 89, 220);
  padding: 12px 20px;
  color: #f9f9f9;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
}
 
.header-actions span {
  padding: 10px;
  text-align: center;
}
 
.list {
  margin-bottom: 40px;
  padding: 25px;
  background-color: #f9f9f9;
  border-radius: 8px;
}
 
.list h2 {
  margin-bottom: 20px;
  color: black;
  font-size: 25px;
  border-bottom: 2px solid black;
  padding-bottom: 10px;
}
 
.doctors-departments-container {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}
 
.doctors-departments-container .list.doctors {
  flex: 2;
}
 
.doctors-departments-container .list.departments {
  flex: 1;
}
 
.appointments-container {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}
 
.appointments-container .list {
  flex: 1;
}
 
.search-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
 
.search-bar select,
.search-bar input {
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
}
 
.search-bar input {
  flex: 1;
}
 
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9;
}
 
table th {
  background-color: #2468b0;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 500;
  font-size: 16px;
}
 
table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
}
 
table a {
  text-decoration: none;
  color: #007bff;
  margin-right: 10px;
  font-size: 14px;
}
 
table button {
  background-color: #007bff;
  color: white;
  cursor: pointer;
  font-size: 14px;
  padding: 8px;
  border: none;
  margin-right: 5px;
}
</style>