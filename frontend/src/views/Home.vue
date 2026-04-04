

<template>
    <div>
    <RouterLink to="/login"> Admin View</RouterLink>
    <RouterLink to="/login"> Patient View</RouterLink>
    <RouterLink to="/login"> Doctor View</RouterLink>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

