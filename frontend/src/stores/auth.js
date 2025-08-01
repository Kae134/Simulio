import { jwtDecode } from 'jwt-decode'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || ''
    }),
    getters: {
        isAuthenticated: (state) => {
            console.log(state, "test")
            if (!state.token) return false
            try {
                const { exp } = jwtDecode(state.token)
                return Date.now() < exp * 1000
            } catch {
                return false
            }
        }
    },
    actions: {
        login(token) {
            try {
                const { exp } = jwtDecode(token)
                if (Date.now() >= exp * 1000) {
                    throw new Error('Token expiré.')
                }
                this.token = token
                localStorage.setItem('token', token)
            } catch (err) {
                console.log('Token invalide :', err.message)
                this.logout()
                throw err
            }
        },
        logout() {
            this.token = ''
            localStorage.removeItem('token')
        },
        getAuthHeader() {
            return { Authorization: `Bearer ${this.token}` }
        },
        decodeToken() {
            try {
                return this.token ? jwtDecode(this.token) : null
            } catch {
                return null
            }
        }
    }
})
