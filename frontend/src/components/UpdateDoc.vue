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
        <div>
        <h2>Update Doctor</h2>
        <form @submit.prevent="updateDoctor">
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
                <input type="password" id="password" v-model="Doctorform.password" placeholder="Leave it blank if don't want any change" />
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
                    <option v-for="depart in departments" :key="depart.department_id" :value="depart.department_id">
                        {{ depart.department_name }}
                    </option>
                </select>
            </div>
 
            <button type="submit">Edit Doctor</button>
            <button type="button" @click="emit('cancelEdit')">Cancel</button>
        </form>
    </div>
</template>