<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import AddDepartment from './AddDepartment.vue'
import AddDoctor from './AddDoctor.vue'

const router = useRouter()
const username = localStorage.getItem('username')
const token = localStorage.getItem('token')


const docForm = ref(false)
const doctors = ref([])

const departForm = ref(false)
const departments = ref([])

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

const onDoctorAdded = () => {
  showAddDoctorForm()
  docForm.value = false
}

const onDepartmentAdded = () => {
  showAddDepartmentForm()
  departForm.value = false
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/login')
}

onMounted(() => {
  showAddDoctorForm();
  showAddDepartmentForm();
})

</script>

<template>
  <div>
    <h1>Welcome, {{ username }}!</h1>
    <p>You are logged in as an Admin.</p>
    <button @click="logout()">Logout</button>

    <button @click="toggleDocForm">
      {{ docForm ? 'Hide' : 'Add Doctor' }}
    </button>
    <AddDoctor v-if="docForm" @doctorAdded="onDoctorAdded"/>
        <h2>Doctors</h2>
    <p v-if="doctors.length === 0">No doctors added yet.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Qualification</th>
          <th>Experience (yrs)</th>
          <th>Contact</th>
          <th>Department</th>
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
        </tr>
      </tbody>
    </table>

    <button @click="toggleDepartForm">
      {{ departForm ? 'Hide' : 'Add Department' }}
    </button>

    <AddDepartment v-if="departForm" @departmentAdded="onDepartmentAdded"/>
        <h2>Department</h2>
         <p v-if="departments.length === 0">No departments added yet.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="department in departments" :key="department.department_id">
          <td>{{ department.department_name }}</td>
          <td>{{ department.department_description }}</td>
        </tr>
      </tbody>
    </table>
    
  </div>
</template>