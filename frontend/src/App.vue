<template>
  <div class="flex flex-col items-center font-primary min-h-screen">
    <nav 
      v-if="!isAuthPage"
      class="flex gap-4 p-4 text-black w-full justify-between absolute bg-white z-100"
    >
      <router-link to="/">
        <img :src="logoImage" alt="" class="w-24 cursor-pointer hover:opacity-80 transition-opacity">
      </router-link>
      <div class="flex w-fit gap-4 items-center">
        <template v-if="auth.isAuthenticated">
          <router-link to="/dashboard" class="hover:text-simugreen-500">Dashboard</router-link>
          <span>|</span>
          <router-link to="/simulate" class="hover:text-simugreen-500">Simulation</router-link>
          <span>|</span>
          <button 
            @click="logout"
            class="rounded-md bg-red-500 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg hover:bg-red-400"
          >
            Logout
          </button>
        </template>
        
        <template v-else>
          <router-link 
            class="rounded-md bg-simugreen-500 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg hover:bg-simugreen-400" 
            to="/login"
          >
            Login
          </router-link>
        </template>
      </div>
    </nav>
    
    <router-view :class="isAuthPage ? 'flex-1' : ''" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter, useRoute } from 'vue-router'
import logoImage from '@/assets/icons/Simulio_logo.svg'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const authPages = ['/login','/dashboard']
const isAuthPage = computed(() => authPages.includes(route.path))

const logout = () => {
  auth.logout()
  router.push('/')
}
</script>