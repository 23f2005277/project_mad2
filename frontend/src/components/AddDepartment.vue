<script setup>
import { reactive } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const Departform = reactive({
    department_name: '',
    department_desc: ''
})

const toast = useToast();
const emit = defineEmits(['departmentAdded']);

const addDepartment = async () => {
    const token = localStorage.getItem('token')
    const newDepartment = {
        department_name: Departform.department_name,
        department_desc: Departform.department_desc
    };

    try {
        const response = await axios.post('http://127.0.0.1:5001/api/add_department', newDepartment, {
            headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Department added successfully');
        emit('departmentAdded');
        Object.keys(Departform).forEach(key => Departform[key] = '')
    } catch (error) {
        toast.error('Failed to add department');
        console.error(error.response);
    }
}
</script>


<template>
    <div>
        <h2>Add Department</h2>
        <form @submit.prevent="addDepartment">
            <div>
                <label for="department_name">Department Name:</label>
                <input type="text" id="department_name" v-model="Departform.department_name" required />
            </div>
            <div>
                <label for="department_desc">Description:</label>
                <textarea id="department_desc" v-model="Departform.department_desc" rows="3"></textarea>
            </div>
            <button type="submit">Add Department</button>
        </form>
    </div>
</template>