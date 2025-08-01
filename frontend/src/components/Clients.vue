<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import PlusIcon from '@/assets/icons/plus.svg'
import ReloadIcon from '@/assets/icons/reload.svg'
import CloseIcon from '@/assets/icons/close.svg'
import ResultItem from '@/components/ResultItem.vue'
import { pop_up } from '@/stores/popUpStore'

const auth = useAuthStore()
const clients = ref(null)
const panelRef = ref(null)

const form = ref({
    name: '',
    email: '',
    phone: '',
})

const createUser = async () => {
    try {
        const response = await axios.post('http://localhost:8000/api/v1/clients/create', form.value, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Client créé:', response.data)
        pop_up('Client créé avec succès!', 'success')
        getClients()
    } catch (err) {
        pop_up('Échec de la création du client.', 'error')
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
        pop_up('Erreur lors de la récupération des clients:', 'error')
    }
}

const userDetails = ref(
    {
    name: '',
    email: '',
    phone: '',
    total_simulations: 0,
    last_simulation_date: null,
    list_simulations: []
    }
    )
    // { "name": "string", "email": "user@example.com", "phone": "0610054442", "id": 2, "user_id": 1, "created_at": "2025-07-29T18:31:02", "list_simulations": { "client": { "id": 2, "name": "string", "email": "user@example.com", "phone": "0610054442", "created_at": "2025-07-29T18:31:02" }, "simulations": [ { "id": 2, "data": { "N": 1, "T": 20, "C2": 1, "ASSU": 5, "mois": "01", "annee": "2026", "apport": 0, "TRAVAUX": 0, "fraisAgence": 20, "fraisNotaire": 10, "revalorisationBien": 10 }, "result": { "A": 0.06575, "C2": 1.315, "df": [ { "Date": "2026-01-01T00:00:00", "Year": 2026, "Intérêts": 0.02, "Mensualité": 0.13, "Capital Amorti": 0.1, "Capital restant dû": 1.215 }, { "Date": "2026-02-01T00:00:00", "Year": 2026, "Intérêts": 0.02, "Mensualité": 0.13, "Capital Amorti": 0.1, "Capital restant dû": 1.1149999999999998 }, { "Date": "2026-03-01T00:00:00", "Year": 2026, "Intérêts": 0.02, "Mensualité": 0.13, "Capital Amorti": 0.1, "Capital restant dû": 1.0149999999999997 }, { "Date": "2026-04-01T00:00:00", "Year": 2026, "Intérêts": 0.02, "Mensualité": 0.13, "Capital Amorti": 0.1, "Capital restant dû": 0.9149999999999996 }, { "Date": "2026-05-01T00:00:00", "Year": 2026, "Intérêts": 0.02, "Mensualité": 0.13, "Capital Amorti": 0.11, "Capital restant dû": 0.8049999999999997 }, { "Date": "2026-06-01T00:00:00", "Year": 2026, "Intérêts": 0.01, "Mensualité": 0.13, "Capital Amorti": 0.11, "Capital restant dû": 0.6949999999999997 }, { "Date": "2026-07-01T00:00:00", "Year": 2026, "Intérêts": 0.01, "Mensualité": 0.13, "Capital Amorti": 0.11, "Capital restant dû": 0.5849999999999997 }, { "Date": "2026-08-01T00:00:00", "Year": 2026, "Intérêts": 0.01, "Mensualité": 0.13, "Capital Amorti": 0.11, "Capital restant dû": 0.47499999999999976 }, { "Date": "2026-09-01T00:00:00", "Year": 2026, "Intérêts": 0.01, "Mensualité": 0.13, "Capital Amorti": 0.11, "Capital restant dû": 0.36499999999999977 }, { "Date": "2026-10-01T00:00:00", "Year": 2026, "Intérêts": 0.01, "Mensualité": 0.13, "Capital Amorti": 0.12, "Capital restant dû": 0.24499999999999977 }, { "Date": "2026-11-01T00:00:00", "Year": 2026, "Intérêts": 0, "Mensualité": 0.13, "Capital Amorti": 0.12, "Capital restant dû": 0.12499999999999978 }, { "Date": "2026-12-01T00:00:00", "Year": 2026, "Intérêts": 0, "Mensualité": 0.13, "Capital Amorti": 0.12, "Capital restant dû": 0.004999999999999782 } ], "TRAVAUX": 0, "interet": 0.21252250305592235, "output2": [ { "Apport": 0, "Prix du bien": 1, "Frais d'agence": 0.2, "Frais de notaire": 0.1, "Garantie Bancaire": 0.015, "Total à financer": 1.315 } ], "output3": [ { "Taux d'assurance": 5, "Taux d'intérêt": 20, "Mensualité de crédit": 0.13, "Montant du prêt total": 1.315 } ], "output4": [ { "Date d'acquisition": "01/01/2026", "Fin du financement": "01/01/2027" } ], "output13": [ { "Prix du bien": 1, "Capital restant dû": 0.004999999999999782, "Somme disponible en cas de revente": 0.9950000000000002 }, { "Prix du bien": 1.1, "Capital restant dû": 0, "Somme disponible en cas de revente": 1.1 } ], "mensualite": 0.12729354192132686, "fraisAgence2": 0.2, "fraisNotaire": 0.1, "salaireMinimum": 0, "garantieBancaire": 0.015 }, "created_at": "2025-07-29T18:55:42", "client_id": 2, "summary": { "mensualite": 0.12729354192132686, "capital": 1, "duree_annees": 1, "taux": 20 } }, { "id": 1, "data": { "N": 1, "T": 20, "C2": 1, "ASSU": 5, "mois": "01", "annee": "2026", "apport": 0, "TRAVAUX": 0, "fraisAgence": 20, "fraisNotaire": 10, "revalorisationBien": 10 }, "result": { "additionalProp1": {} }, "created_at": "2025-07-29T18:51:25", "client_id": 2, "summary": { "mensualite": 0, "capital": 1, "duree_annees": 1, "taux": 20 } } ], "total": 2, "skip": 0, "limit": 100, "stats": { "total_simulations": 2, "average_capital": 1, "last_simulation": "2025-07-29T18:55:42" } } }




const getDetailsClient = async (id) => {
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/clients/${id}`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Détails du client récupérés:', response.data)
        userDetails.value = response.data
    } catch (err) {
        pop_up('Erreur lors de la récupération des détails du client:', 'error')
    }
}

const getSimulationsClient = async (id) => {
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/clients/${id}/simulations`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Simulations du client récupérées:', response.data)
        userDetails.value.list_simulations = response.data
    } catch (err) {
        pop_up('Erreur lors de la récupération des simulations du client:', 'error')
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

const seeMoreOfUser = ref(false)
const idUserDetails = ref(null)

const toggleSeeMoreUser = (id) => {
    seeMoreOfUser.value = !seeMoreOfUser.value
    idUserDetails.value = id
    console.log('ID utilisateur pour détails:', idUserDetails.value);
    getDetailsClient(idUserDetails.value)
    getSimulationsClient(idUserDetails.value)
    console.log('See more user display toggled:', seeMoreOfUser.value)
}

function handleClickOutside(event) {
    if (panelRef.value && !panelRef.value.contains(event.target)) {
        seeMoreOfUser.value = false
    }
}

</script>

<template>
    <div class="flex flex-col items-start justify-start p-16 gap-4 w-full min-h-1/2">
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
                    <div v-if="clients && clients.clients" class="flex flex-col w-full">
                        <div v-for="client in clients.clients" :key="client.id" class="flex p-4 bg-white w-full border-b-2 border-slate-200 hover:bg-slate-50 transition duration-300 ease">
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
                <form @submit.prevent="createUser" class="flex flex-col gap-4">
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
                            Retour
                        </button>
                    </div>

                </form>
            </div>
        </div>
        

        <div v-if="seeMoreOfUser === true" class="fixed inset-0 bg-black/10 backdrop-blur z-10 flex items-center justify-end"  @click="handleClickOutside">
            <div ref="panelRef" class="relative flex flex-col items-start justify-start z-100 bg-white p-16 rounded-sm shadow-md w-1/2 h-full gap-8">
                <button @click="seeMoreOfUser = false" class="absolute top-1 left-1 bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-simuiolet-200">
                    <img :src="CloseIcon" alt="close" class="w-8 h-8">
                </button>
                <h1 class="text-2xl font-light">Details</h1>
                <div>
                    <hr class="w-full h-1 text-transparent bg-slate-200/50 mb-4 mt-4">
                    <h1 class="text-xl font-semibold mt-4">Informations : </h1>
                    <div class="flex flex-col gap-2 p-4">
                        <p class="text-lg"><strong>Nom :</strong> {{ userDetails.name }}</p>
                        <p class="text-lg"><strong>Email :</strong> {{ userDetails.email }}</p>
                        <p class="text-lg"><strong>Téléphone :</strong> {{ userDetails.phone }}</p>
                        <p class="text-lg"><strong>ID :</strong> {{ userDetails.id }}</p>
                        <p class="text-lg"><strong>User ID :</strong> {{ userDetails.user_id }}</p>
                        <p class="text-lg"><strong>Créé le :</strong> {{ userDetails.created_at }}</p>
                    </div>
                    <hr class="w-full h-1 text-transparent bg-slate-200/50 mb-4 mt-4">
                    <div class="h-full flex flex-col gap-4">
                        <h2 class="text-xl font-semibold mt-4">Simulations</h2>
                        <div v-if="userDetails.list_simulations" class="flex flex-col w-full h-1/2 overflow-y-scroll">
                            <div
                                v-for="simulation in userDetails.list_simulations.simulations"
                                :key="simulation.id"
                                class="flex flex-wrap gap-4 p-4 bg-white w-full border-b-2 border-slate-200 hover:bg-slate-50 transition duration-300 ease"
                            >

                                <ResultItem label="Prix du bien" :value="simulation?.data?.C2" :border="false"/>
                                <ResultItem label="Frais de notaire" :value="simulation?.result?.fraisNotaire" :border="false"/>
                                <ResultItem label="Garantie bancaire" :value="simulation?.result?.garantieBancaire" :border="false"/>
                                <ResultItem label="Travaux" :value="simulation?.data?.TRAVAUX" :border="false"/>
                                <ResultItem label="Frais d'agence" :value="simulation?.result?.output2?.[0]?.['Frais d\'agence']" :border="false"/>
                                <ResultItem label="Total à financer" :value="simulation?.result?.output3?.[0]?.['Montant du prêt total']" :border="false" />
                                <ResultItem label="Revenu acquéreur minimum mensuel" :value="simulation?.result?.salaireMinimum" :border="false" />
                            </div>

                        </div>
                        <p v-if="!userDetails.list_simulations || userDetails.list_simulations.simulations.length === 0" class="text-gray-200">Aucune simulation trouvée pour ce client.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
