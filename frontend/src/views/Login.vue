<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'
    import axios from 'axios'
    import Arrow from '@/assets/icons/arrow-left.svg'

    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const auth = useAuthStore()

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/v1/auth/login', new URLSearchParams({
            username: email.value,
            password: password.value
            }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })

            auth.login(response.data.access_token)
            router.push('/dashboard')
        } catch (err) {
            alert('Échec de connexion.')
        }
    }
</script>


<template>
    <div class="flex items-center justify-center w-full flex-1">
        <div class="flex flex-col items-center justify-center w-1/2 p-24 gap-12 h-screen bg-white bg-gradient-to-r from-simugreen-400/30 via-simugreen-400/50 to-simugreen-400/70">
            <h1 class="text-white text-8xl font-bold">Welcome to Simulio</h1>
            <h2 class="text-white text-4xl font-light"><span class="font-bold">Boostez vos ventes immobilières</span>
            Grâce aux simulateurs les plus puissants du marché</h2>
        </div>
        <div class="flex items-center justify-center bg-white w-1/2 h-screen">
            <div class="flex flex-col items-center justify-center w-164">
                <h1 class="text-4xl font-light text-gray-800 mb-16">Login</h1>
                <form @submit.prevent="handleLogin" class="flex flex-col w-full">
                    <input 
                        v-model="email" 
                        type="email" 
                        placeholder="Email"
                        class="w-full bg-transparent mb-8 placeholder:text-slate-500 focus:text-simugreen-600 text-simugreen-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simugreen-200 hover:border-simugreen-100 shadow-sm focus:shadow"
                    />
                    <input 
                        v-model="password" 
                        type="password" 
                        placeholder="Password"
                        class="w-full bg-transparent mb-8 placeholder:text-slate-500 focus:text-simugreen-600 text-simugreen-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simugreen-200 hover:border-simugreen-100 shadow-sm focus:shadow"
                    />
                    <button 
                        type="submit"
                        class="rounded-md bg-simugreen-500 mb-8 py-2 px-4 border border-transparent text-center text-lg text-white transition-all shadow-md hover:shadow-lg hover:bg-simugreen-400" 
                    >
                        Login
                    </button>
                </form>
                <router-link to="/" class="flex items-center justify-center">
                    <img :src="Arrow" class="w-8" alt="">
                    <span class="link link-underline link-underline-black text-black">
                        back
                    </span>
                </router-link>
            </div>
        </div>
    </div>
</template>