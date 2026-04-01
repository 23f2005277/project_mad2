<script setup>
import { reactive, onMounted, ref } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const token = localStorage.getItem('token');
const toast = useToast();
const emit = defineEmits(['departmentUpdated']);
const props = defineProps(['department']);

const Departform = reactive({
    department_name: props.department.department_name,
    department_desc: props.department.department_description
})

const updateDepartment = async () => {
    try {
        const response = await axios.put(`http://127.0.0.1:5001/api/update_department/${props.department.department_id}`, Departform, {
            headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Department updated successfully!')
        emit('departmentUpdated')
    } catch (error) {
        toast.error('Failed to update department.')
        console.error('Error while updating department:', error.response)
    }
}
</script>

<template>
    <div>
        <h2>Update Department</h2>
        <form @submit.prevent="updateDepartment">
            <div>
                <label for="department_name">Department Name:</label>
                <input type="text" id="department_name" v-model="Departform.department_name" required />
            </div>
            <div>
                <label for="department_desc">Description:</label>
                <textarea id="department_desc" v-model="Departform.department_desc" rows="3"></textarea>
            </div>
            <button type="submit">Edit Department</button>
            <button type="button" @click="emit('cancelEdit')">Cancel</button>
        </form>
    </div>
</template>