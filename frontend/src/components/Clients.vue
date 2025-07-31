<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import PlusIcon from '@/assets/icons/plus.svg'
import ReloadIcon from '@/assets/icons/reload.svg'

const auth = useAuthStore()
const clients = ref(null)

const form = ref({
    name: '',
    email: '',
    phone: '',
})

const success = ref(false)
const error = ref('')

const submitForm = async () => {
    try {
        const response = await axios.post('http://localhost:8000/api/v1/clients/create', form.value, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        success.value = true
        error.value = ''
        console.log('Client créé:', response.data)
        getClients()
    } catch (err) {
        error.value = 'Échec de la création du client.'
        success.value = false
        console.error('Erreur lors de la création du client:', err)
    }
}

const getClients = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/v1/clients/', {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Clients récupérés:', response.data)
        clients.value = response.data
    } catch (err) {
        console.error('Erreur lors de la récupération des clients:', err)
    }
}

const userDetails = ref({
    name: '',
    email: '',
    phone: '',
    total_simulations: 0,
    last_simulation_date: null,
    list_simulations: []
})

const getDetailsClient = async (id) => {
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/clients/${id}`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Détails du client récupérés:', response.data)
        userDetails.value = response.data
    } catch (err) {
        console.error('Erreur lors de la récupération des détails du client:', err)
    }
}

onMounted(async () => {
    await getClients()
    console.log('Clients récupérés:', clients.value.clients)
})

// REMOVE TEST WHEN DONE
const test = { "clients": [ { "id": 2, "name": "string", "email": "user@example.com", "phone": "0610054442", "stats": { "total_simulations": 2, "last_simulation_date": "2025-07-29T18:55:42" } }, { "id": 4, "name": "test", "email": "test@gmail.com", "phone": "0649009373", "stats": { "total_simulations": 0, "last_simulation_date": null } }, { "id": 5, "name": "test", "email": "johndoe@gmail.com", "phone": "0649009373", "stats": { "total_simulations": 0, "last_simulation_date": null } } ], "total": 3, "message": "Sélectionnez un client pour enregistrer la simulation" }

const addUserDisplay = ref(false)

const toggleAddUserDisplay = () => {
    addUserDisplay.value = !addUserDisplay.value
    console.log('Add user display toggled:', addUserDisplay.value)
}

const isRotating = ref(false)

const Reload = async () => {
    getClients()
    isRotating.value = true
    await new Promise(resolve => setTimeout(resolve, 500))
    isRotating.value = false
}

const seeMoreUser = ref(false)
const idUserDetails = ref(null)

const toggleSeeMoreUser = (id) => {
    seeMoreUser.value = !seeMoreUser.value
    idUserDetails.value = id
    console.log('See more user display toggled:', seeMoreUser.value)
}

</script>

<template>
    <div class="flex flex-col items-start justify-start p-16 gap-4 w-full min-h-1/2 gap-16">
        <h1 class="text-2xl font-light mb-4">Gestion des clients</h1>
        <div class="flex flex-col w-full gap-4">
            <div>
                <button class="flex items-center gap-2 cursor-pointer text-lg" @click="toggleAddUserDisplay()"><img :src="PlusIcon" class="w-5" alt=""><span class="link-underline link-underline-black">Add user</span></button>
            </div>
            <div class="flex flex-col items-center justify-between w-full">
                <div class="flex items-center w-full justify-start gap-4 p-4 font-semibold">
                    <p class="w-32">Name</p>
                    <p class="w-64">Email</p>
                    <p class="w-48">Numero de telephone</p>
                    <p class="w-32">Nb simulation</p>
                    <img @click="() => {Reload()}" :src="ReloadIcon" :class="[
                        'w-4 cursor-pointer transition-transform duration-500',
                        isRotating ? 'rotate-180' : 'rotate-0']" 
                    alt="">
                </div>
                <hr class="w-full h-1 text-transparent bg-slate-400/50">
                <div class="flex flex-col w-full h-128 mb-8 overflow-y-scroll bg-white">
                    <div v-if="test && test.clients" class="flex flex-col w-full">
                        <div v-for="client in test.clients" :key="client.id" class="flex p-4 bg-white w-full border-b-2 border-slate-200 hover:bg-slate-50 transition duration-300 ease">
                            <p class="text-lg w-32 overflow-hidden text-ellipsis mr-4">
                                {{ client.name }}
                            </p>
                            <a :href="`mailto:${client.email}`" class="text-lg w-64 overflow-hidden text-ellipsis mr-4 underline text-blue-600 hover:text-blue-800">
                                {{ client.email }}
                            </a>
                            <p class="text-lg w-48 overflow-hidden text-ellipsis mr-4">
                                {{ client.phone }}
                            </p>
                            <p class="text-lg w-32 overflow-hidden text-ellipsis mr-4">
                                {{ client.stats.total_simulations }}
                            </p>
                            <button @click="toggleSeeMoreUser(client.id)" class="text-lg w-64 overflow-hidden text-ellipsis mr-4 underline text-black hover:font-semibold transition duration-3500 ease">Voir plus</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div v-if="addUserDisplay === true" class="fixed inset-0 bg-black/10 backdrop-blur-sm z-50 flex items-center justify-center">
            <div class="flex flex-col bg-white p-6 rounded shadow-md w-full max-w-md gap-8">
                <h1 class="text-2xl font-light">Ajouter un client</h1>
                <form @submit.prevent="submitForm" class="flex flex-col gap-4">
                    <div class="mb-4">
                        <label for="name">Nom :</label>
                        <input v-model="form.name" type="text" id="name" required maxlength="255"
                            class="w-full bg-transparent placeholder:text-slate-500 focus:text-simuiolet-600 text-simuiolet-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simuiolet-200 hover:border-simuiolet-100 shadow-sm focus:shadow" />
                    </div>

                    <div class="mb-4">
                        <label for="email">Email :</label>
                        <input v-model="form.email" type="email" id="email" required maxlength="255"
                            class="w-full bg-transparent placeholder:text-slate-500 focus:text-simuiolet-600 text-simuiolet-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simuiolet-200 hover:border-simuiolet-100 shadow-sm focus:shadow"/>
                    </div>

                    <div class="mb-4">
                        <label for="phone">Téléphone :</label>
                        <input v-model="form.phone" type="tel" id="phone" required maxlength="20"
                            class="w-full bg-transparent placeholder:text-slate-500 focus:text-simuiolet-600 text-simuiolet-300 text-lg border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simuiolet-200 hover:border-simuiolet-100 shadow-sm focus:shadow"/>
                    </div>

                    <div class="flex justify-between items-center mt-8">
                        <button @click="getClients()" type="submit" class="rounded-md bg-simuiolet-600 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg focus:bg-simuiolet-400 focus:shadow-none active:bg-slate-700 hover:bg-simuiolet-400 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none">
                            Créer le client
                        </button>
                        <button type="button" @click="toggleAddUserDisplay()" class="rounded-md border border-transparent py-2 px-4 text-center text-sm transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none">
                            Annuler
                        </button>
                    </div>

                    <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
                    <p v-if="success" class="text-green-600 mt-2">Client créé avec succès !</p>
                </form>
            </div>
        </div>
        

        <div v-if="addUserDisplay === true" class="fixed inset-0 bg-black/10 backdrop-blur-sm z-50 flex items-center justify-center">
            <div class="flex flex-col bg-white p-6 rounded shadow-md w-full max-w-md gap-8">
                <h1 class="text-2xl font-light">Ajouter un client</h1>
                <p>{{  }}</p>
            </div>
        </div>
    </div>
</template>
