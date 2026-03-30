<script setup>
import {reactive} from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const router = useRouter()
const toast = useToast()

const Loginform = reactive({
    username: '',
    password: '',
})

const performLogin = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5001/api/login', Loginform)
        const { access_token, role, username, email } = response.data.data

        localStorage.setItem('token', access_token)
        localStorage.setItem('role', role)
        localStorage.setItem('username', username)
        localStorage.setItem('email', email)

        toast.success('Login successful')

        if (role == 'admin') {
            router.push('/admin')
        } else if (role == 'patient') {
            router.push('/patient')
        } else {
            router.push('/doctor')
        }
    } catch (error) {
        toast.error('Login failed. Please check your credentials and try again.')
        console.error('Error during login:', error.response)
    }
}

</script>

<template>
      <div>
    <h1>Login</h1>
    <form @submit.prevent="performLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" v-model="Loginform.username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="Loginform.password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
    
</template>