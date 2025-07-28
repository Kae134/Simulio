<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'
    import axios from 'axios'

    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const auth = useAuthStore()

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:8000/login', new URLSearchParams({
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
    <div>
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
            <input v-model="email" type="email" placeholder="Email" />
            <input v-model="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
        </form>
    </div>
</template>