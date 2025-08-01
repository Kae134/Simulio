<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'
    import axios from 'axios'
    import ArrowLeft from '@/assets/icons/arrow-left.svg'
    import ArrowRight from '@/assets/icons/arrow-right.svg'
    import { pop_up } from '@/stores/popUpStore'

    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const auth = useAuthStore()
    const confirmPassword = ref('')

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
            pop_up('Connexion réussie !', 'success')
        } catch (err) {
            pop_up('Échec de connexion.', 'error')
        }
    }

    const handleRegister = async () => {
        try {
            if (password.value !== confirmPassword.value) {
                pop_up('Les mots de passe ne correspondent pas.', 'error')
                return
            }

            const response = await axios.post('http://localhost:8000/api/v1/auth/register', {
                email: email.value,
                password: password.value
            }, {
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })

            pop_up('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            router.push('/login') 
            
        } catch (err) {
            if (err.response?.data?.detail) {
                pop_up(err.response.data.detail, 'error')
            } else {
                pop_up('Échec de l\'inscription.', 'error')
            }
        }
    }

    const swap = ref(false)

    const toggleSwap = () => {
        swap.value = !swap.value
    }


</script>


<template>
    <div class="flex items-center justify-center w-full flex-1">
        <div 
            :style="{ transform: swap ? 'translateX(100%)' : 'translateX(0%)' }"
            class="flex flex-col items-center justify-center w-1/2 p-24 gap-12 h-screen z-10 bg-white bg-gradient-to-r from-simugreen-400/30 via-simugreen-400/50 to-simugreen-400/70 transition-transform duration-700 ease-in-out">
            
            <div v-if="!swap" class="flex flex-col items-start justify-center w-164">
                <h1 class="text-white text-8xl font-bold">Welcome Back !</h1>
                <h2 class="text-white text-4xl font-light"><span class="font-bold">Boostez vos ventes immobilières</span>
                Grâce aux simulateurs les plus puissants du marché</h2>
                    <button @click="toggleSwap()" class="mt-8 flex items-center justify-center text-xl rounded-full border-2 w-64 border-white py-2 px-4 text-center transition-all shadow-sm hover:shadow-lg text-white hover:bg-simugreen-500 hover:border-simugreen-800 focus:text-white focus:bg-simugreen-500 focus:border-simugreen-800 active:border-simugreen-800 active:text-white active:bg-simugreen-400 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none">
                        Register
                        <img :src="ArrowRight" class="w-6 filter brightness-0 invert" alt="">
                    </button>
            </div>
            <div v-else class="flex flex-col items-start justify-center w-164">
                <h1 class="text-white text-8xl font-bold">Welcome to Simulio</h1>
                <h2 class="text-white text-4xl font-light"><span class="font-bold">Boostez vos ventes immobilières</span>
                Grâce aux simulateurs les plus puissants du marché</h2>
                <button @click="toggleSwap()" class="mt-8 flex items-center justify-center text-xl rounded-full border-2 border-white w-64 py-2 px-4 text-center transition-all shadow-sm hover:shadow-lg text-white hover:bg-simugreen-500 hover:border-simugreen-800 focus:text-white focus:bg-simugreen-500 focus:border-simugreen-800 active:border-simugreen-800 active:text-white active:bg-simugreen-400 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none">
                    <img :src="ArrowLeft" class="w-6 filter brightness-0 invert" alt="">
                    Login
                </button>
            </div>
        </div>
        <div 
        :style="{ transform: swap ? 'translateX(-100%)' : 'translateX(0%)' }"
        class="flex items-center justify-center bg-white w-1/2 h-screen transition-transform duration-700 ease-in-out">
            <div v-if="!swap" class="flex flex-col items-center justify-center w-164">
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
                    <img :src="ArrowLeft" class="w-4" alt="">
                    <span class="link link-underline link-underline-black text-black">
                        Back
                    </span>
                </router-link>
            </div>
            <div v-else class="flex flex-col items-center justify-center w-164">
                <h1 class="text-4xl font-light text-gray-800 mb-16">Register</h1>
                <form @submit.prevent="handleRegister" class="flex flex-col w-full">
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
                    <input 
                        v-model="confirmPassword"
                        type="password"
                        placeholder="Confirm Password"
                        class="w-full bg-transparent mb-8 placeholder:text-slate-500 focus:text-simugreen-600 text-simugreen-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simugreen-200 hover:border-simugreen-100 shadow-sm focus:shadow"
                    />
                    <button 
                        type="submit"
                        class="rounded-md bg-simugreen-500 mb-8 py-2 px-4 border border-transparent text-center text-lg text-white transition-all shadow-md hover:shadow-lg hover:bg-simugreen-400"
                    >
                        Register
                    </button>
                </form>
                <router-link to="/" class="flex items-center justify-center">
                    <img :src="ArrowLeft" class="w-4" alt="">
                    <span class="link link-underline link-underline-black text-black">
                        Back
                    </span>
                </router-link>
            </div>
        </div>
    </div>
</template>