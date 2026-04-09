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
    <div class="list">
        <h2>Add Department</h2>
        <form @submit.prevent="addDepartment" class="form-body">
            <div class="form-group">
                <label for="department_name">Department Name:</label>
                <input type="text" id="department_name" v-model="Departform.department_name" required />
            </div>
            <div class="form-group">
                <label for="department_desc">Description:</label>
                <textarea id="department_desc" v-model="Departform.department_desc" rows="3"></textarea>
            </div>
            <div class="form-actions">
                <button type="submit">Add Department</button>
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