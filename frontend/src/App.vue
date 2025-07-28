<template>
  <div>
    <nav>
      <router-link to="/dashboard">Dashboard</router-link> |
      <router-link to="/login">Login</router-link> |
      <button @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
  import { useAuthStore } from './stores/auth'

  const auth = useAuthStore()
  const logout = () => {
    auth.logout()
  }
</script>
