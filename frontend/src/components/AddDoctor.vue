<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const Doctorform = reactive({
    username: '',
    email_id: '',
    password: '',
    name: '',
    qualification: '',
    contact: '',
    experience_years: 0,
    ddepartment_id: ''
});

const token = localStorage.getItem('token')
const toast = useToast();
const emit = defineEmits(['doctorAdded']);
const departments = ref([]);

const addDoctor = async () => {
    const newDoctor = {
        username: Doctorform.username,
        email_id: Doctorform.email_id,
        password: Doctorform.password,
        name: Doctorform.name,
        qualification: Doctorform.qualification,
        contact: Doctorform.contact,
        experience_years: Doctorform.experience_years,
        ddepartment_id: Doctorform.ddepartment_id
    };

    try {
        const response = await axios.post('http://127.0.0.1:5001/api/add_doctor', newDoctor, {
            headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Doctor added successfully!');
        emit('doctorAdded');
        Object.keys(Doctorform).forEach(key => Doctorform[key] = '');
    } catch (error) {
        toast.error('Could not add doctor.');
        console.error('Error while adding doctor:', error.response)
    }
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/api/alldepartments', {
      headers: { Authorization: `Bearer ${token}` }
    });
    departments.value = response.data.data;
  } catch (error) {
    console.error('Error in loading departments:', error.response);
  }
})

</script>

<template>
    <div class="list">
        <h2>Add Doctor</h2>
        <form @submit.prevent="addDoctor" class="form-body">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="Doctorform.username" required />
            </div>
            <div class="form-group">
                <label for="email_id">Email:</label>
                <input type="email" id="email_id" v-model="Doctorform.email_id" required />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="Doctorform.password" required />
            </div>
            <div class="form-group">
                <label for="name">Full Name:</label>
                <input type="text" id="name" v-model="Doctorform.name" required />
            </div>
            <div class="form-group">
                <label for="qualification">Qualification:</label>
                <input type="text" id="qualification" v-model="Doctorform.qualification" required />
            </div>
            <div class="form-group">
                <label for="contact">Contact:</label>
                <input type="text" id="contact" v-model="Doctorform.contact" required />
            </div>
            <div class="form-group">
                <label for="experience_years">Experience (years):</label>
                <input type="number" id="experience_years" v-model="Doctorform.experience_years" min="0" required />
            </div>
            <div class="form-group">
                <label for="ddepartment_id">Department:</label>
                <select id="ddepartment_id" v-model="Doctorform.ddepartment_id" required>
                    <option value="" disabled>Select a department</option>
                    <option v-for="depart in departments" :key="depart.department_id" :value="depart.department_id">
                        {{ depart.department_name }}
                    </option>
                </select>
            </div>
            <div class="form-actions">
                <button type="submit">Add Doctor</button>
            </div>
        </form>
    </div>
</template>
 
<style scoped>
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
 
.form-body {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
 
.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
 
.form-group label {
    font-weight: 500;
    font-size: 15px;
}
 
.form-group input,
.form-group textarea,
.form-group select {
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
}
 
.form-actions {
    display: flex;
    gap: 10px;
}
 
.form-actions button {
    background-color: #007bff;
    color: white;
    cursor: pointer;
    font-size: 14px;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
}
</style>
