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
    <div class="page-wrapper">
 
        <header>
            <div>
                <h1>Department Details</h1>
                <p v-if="department">{{ department.department_name }}</p>
            </div>
            <div class="header-actions">
                <a @click="router.go(-1)" class="primary">Back</a>
            </div>
        </header>
 
        <div v-if="department">
            <div class="appoint">
                <h2>{{ department.department_name }}</h2>
                <p class="dept-desc">{{ department.department_description }}</p>
            </div>
 
            <div class="appoint">
                <h2>Doctors</h2>
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
                                    <button class="secondary-c">Book Slot</button>
                                </RouterLink>
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
 
.dept-desc {
    font-size: 15px;
    color: #444;
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
 
.secondary-c {
    background-color: rgb(29, 144, 29);
    color: #f9f9f9;
    font-weight: 600;
}
</style>