<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const router = useRouter();

const Registerform = reactive({
    username: '',
    email_id: '',
    password: ''
});

const toast = useToast();

const RegisterPatient= async () => {
    const registerData = {
        username: Registerform.username,
        email_id: Registerform.email_id,
        password: Registerform.password,
    };

    try {
        const response = await axios.post('http://127.0.0.1:5001/api/register', registerData);
        toast.success('Registration successful!');
        router.push('/login');
    } catch (error) {
        toast.error('Registration failed. Please try again.');
        console.error('Error during registration:', error.response);
    }
};

</script>

<template>
<div>
    <h1>Patient Registration</h1>
    <form @submit.prevent="RegisterPatient">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" v-model="Registerform.username" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="Registerform.email_id" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="Registerform.password" required>
        </div>
        <button type="submit">Register</button>

    </form>
</div>

</template>