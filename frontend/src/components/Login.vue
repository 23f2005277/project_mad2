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
  <div class="page-wrapper">
    <header>
      <h1>Hospital Management System</h1>
      <div class="header-actions">
        <span>Please log in to continue</span>
      </div>
    </header>
 
    <div class="list">
      <h2>Login</h2>
      <form @submit.prevent="performLogin" class="form-body">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" name="username" v-model="Loginform.username" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" name="password" v-model="Loginform.password" required />
        </div>
        <div class="links">
          <button type="submit" class="btn-primary">Login</button>
          <RouterLink to="/register" class="btn-link">Register as Patient</RouterLink>
        </div>
      </form>
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
  flex-direction: column;
  gap: 15px;
  font-size: 18px;
}
 
.header-actions span {
  padding: 10px;
  text-align: center;
}
 
.list {
  margin: 40px auto;
  padding: 25px;
  background-color: #f9f9f9;
  border-radius: 8px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
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
 
.form-group input {
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
}
 
.links {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  margin-top: 5px;
}
 
.btn-primary {
  background: rgb(89, 89, 220);
  color: #f9f9f9;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
}
 
.btn-link {
  text-decoration: none;
  background: rgb(89, 89, 220);
  padding: 12px 20px;
  color: #f9f9f9;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
}
</style>