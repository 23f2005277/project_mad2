<script setup>
import { ref, onMounted } from 'vue'
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

const thisDoctor = ref(null)
const thisDpt = ref(null)


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
  router.push('/login')
}

onMounted(() => {
  showAddDoctorForm();
  showAddDepartmentForm();
  showAllPatients();
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

    <UpdateDoc v-if="thisDoctor" :doctor="thisDoctor" @doctorUpdated="onDoctorUpdated" @cancelEdit="thisDoctor = null"/>

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

    <UpdateDpt v-if="thisDpt" :department="thisDpt" @departmentUpdated="onDepartmentUpdated" @cancelEdit="thisDpt = null"/>

    <h2>Patients</h2>
<p v-if="patients.length === 0">No patients registered yet.</p>
<table v-else>
    <thead>
        <tr>
            <th>Name</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="patient in patients" :key="patient.patient_id">
            <td>{{ patient.name }}</td>
            <td> <RouterLink :to="`/patient_info/${patient.patient_id}`">
                    <button>View</button>
                </RouterLink>
                <button @click="deletePatient(patient.patient_id)">Delete</button>
            </td>
        </tr>
    </tbody>
</table>


  </div>
</template>