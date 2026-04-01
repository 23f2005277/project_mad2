<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRoute, RouterLink, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const departmentId = route.params.id;
const token = localStorage.getItem("token");

const department = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:5001/api/department/${departmentId}`
        , {
            headers: { Authorization: `Bearer ${token}` }
        }
    );
    department.value = response.data.data;
  } catch (error) {
    console.error("Error fetching department details:", error);
  }
});
</script>

<template>
  <div>
    <h1>Department Details</h1>
    <div v-if="department">
      <h2>{{ department.department_name }}</h2>
      <p>{{ department.department_description }}</p>
 
      <h3>Doctors</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Qualification</th>
            <th>Experience (yrs)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doctor in department.doctors" :key="doctor.doctor_id">
            <td>{{ doctor.doctor_name }}</td>
            <td>{{ doctor.doctor_qualification }}</td>
            <td>{{ doctor.doctor_experience_years }}</td>
            <td>
              <RouterLink :to="`/book_slot/${doctor.doctor_id}`">
                <button>Book Slot</button>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="router.go(-1)">Back</button>
  </div>
</template>