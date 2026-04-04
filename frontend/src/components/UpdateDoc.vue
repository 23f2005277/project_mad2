<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const token = localStorage.getItem('token');
const toast = useToast();
const emit = defineEmits(['doctorUpdated']);
const props = defineProps(['doctor']);
const departments = ref([]);

const Doctorform = reactive({
    username: props.doctor.username,
    email_id: props.doctor.email,
    password: '',
    name: props.doctor.name,
    qualification: props.doctor.qualification,
    contact: props.doctor.contact,
    experience_years: props.doctor.experience_years,
    ddepartment_id: props.doctor.ddepartment_id
})

const updateDoctor = async () => {
    try {
        const response = await axios.put(`http://127.0.0.1:5001/api/update_doctor/${props.doctor.doctor_id}`, Doctorform, {
            headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Doctor updated successfully!')
        emit('doctorUpdated')
    } catch (error) {
        toast.error('Failed to update doctor.')
        console.error('Error while updating doctor:', error.response)
    }
}

onMounted(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/api/alldepartments', {
            headers: { Authorization: `Bearer ${token}` }
        })
        departments.value = response.data.data
        Doctorform.ddepartment_id = props.doctor.ddepartment_id
    } catch (error) {
        console.error('Error while loading departments:', error.response)
    }
})

</script>

<template>
    <div class="list">
        <h2>Update Doctor</h2>
        <form @submit.prevent="updateDoctor" class="form-body">
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
                <input type="password" id="password" v-model="Doctorform.password" placeholder="Leave blank to keep unchanged" />
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
                <button type="submit">Save Changes</button>
                <button type="button" class="btn-cancel" @click="emit('cancelEdit')">Cancel</button>
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
 
.form-actions .btn-cancel {
    background-color: rgb(226, 58, 58);
}
</style>
