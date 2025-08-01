import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Simulation from '../views/Simulation.vue'
import Homepage from '../views/Homepage.vue'
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import { jwtDecode } from 'jwt-decode'

const routes = [
    { path: '/login', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/simulate', name: 'Simulation', component: Simulation, meta: { requiresAuth: true } },
    { path: '/', name: 'Home',  component: Homepage, meta: { requiresAuth: false } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, _, next) => {
    const auth = useAuthStore()
    const { token } = storeToRefs(auth)
    console.log('token in router:', token.value)

    const isAuthenticated = computed(() => {
        if (!token.value) return false
        try {
            const { exp } = jwtDecode(token.value)
            return Date.now() < exp * 1000
        } catch {
            return false
        }
    })

    console.log('isAuthenticated:', isAuthenticated.value, 'to:', to.fullPath)

    if (to.meta.requiresAuth && !isAuthenticated.value) {
        console.log('Redirecting to /')
        next('/')
    } else if (to.path === '/login' && isAuthenticated.value) {
        console.log('Redirecting to /dashboard')
        next('/dashboard')
    } else {
        next()
    }
})

export default router
