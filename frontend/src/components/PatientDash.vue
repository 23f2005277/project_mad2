<script setup>
const username = localStorage.getItem('username')
</script>

<template>
  <div>
    <h1>Welcome, {{ username }}!</h1>
    <p>You are logged in as a Patient.</p>
  </div>
</template>