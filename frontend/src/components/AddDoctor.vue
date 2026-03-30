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
    <div>
    <h2>Add Doctor</h2>
    <form @submit.prevent="addDoctor">
 
      <h3>Details</h3>
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="Doctorform.username" required />
      </div>
      <div>
        <label for="email_id">Email:</label>
        <input type="email" id="email_id" v-model="Doctorform.email_id" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="Doctorform.password" required />
      </div>
      <div>
        <label for="name">Full Name:</label>
        <input type="text" id="name" v-model="Doctorform.name" required />
      </div>
      <div>
        <label for="qualification">Qualification:</label>
        <input type="text" id="qualification" v-model="Doctorform.qualification" required />
      </div>
      <div>
        <label for="contact">Contact:</label>
        <input type="text" id="contact" v-model="Doctorform.contact" required />
      </div>
      <div>
        <label for="experience_years">Experience (years):</label>
        <input type="number" id="experience_years" v-model="Doctorform.experience_years" min="0" required />
      </div>
      <div>
        <label for="ddepartment_id">Department:</label>
        <select id="ddepartment_id" v-model="Doctorform.ddepartment_id" required>
          <option value="" disabled>Select a department</option>
          <option v-for="depart in departments" :key="depart.department_id" :value="depart.department_id">{{ depart.department_name }}</option>

        </select>
      </div>
 
      <button type="submit">Add Doctor</button>
    </form>
  </div>



</template>