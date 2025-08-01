<script setup>
import { reactive, ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import Calendar from '@/assets/icons/calendar.svg'

import ResultItem from '@/components/ResultItem.vue'

import Separator from './Separator.vue'
import {pop_up} from '@/stores/popUpStore.js'


const auth = useAuthStore()
const loading = ref(false)
const result = ref(null)
const panelRef = ref(null)

const date = ref(new Date());

console.log('Mois:', String(date.value.getMonth() + 1).padStart(2, '0'))
console.log('Année:', date.value)

watch(date, (newValue, oldValue) => {
    console.log(`Date changée de "${oldValue}" vers "${newValue}"`)
    
    console.log('Mois:', String(newValue.getMonth() + 1).padStart(2, '0'))
    console.log('Année:', String(newValue.getFullYear()))

    console.log('Mois:', String(date.value.getMonth() + 1).padStart(2, '0'))
    console.log('Année:', String(date.value.getFullYear()))
})

const format = (value) => {
    if (typeof value === 'number') {
        return value.toFixed(2)
    }
    console.log(value)
    return '—'
}

const moisEnLettres = {
    1: 'janvier',
    2: 'février',
    3: 'mars',
    4: 'avril',
    5: 'mai',
    6: 'juin',
    7: 'juillet',
    8: 'août',
    9: 'septembre',
    10: 'octobre',
    11: 'novembre',
    12: 'décembre',
};

const form = reactive({
    N: 25,
    C2: 834000,
    T: 3.5,
    ASSU: 0.32,
    apport: 50000,
    mois: String(date.value.getMonth() + 1).padStart(2, '0'),
    annee: String(date.value.getFullYear()),
    fraisAgence: 3,
    fraisNotaire: 7.5,
    TRAVAUX: 20000,
    revalorisationBien: 1
})

const fields = [
    { label: "Prix du bien", id: "C2", type: "slider", model: "C2", attrs: { step: 0.01, required: true } ,'min-max':[0, 3000000]}, 
    { label: "Montant des travaux", id: "TRAVAUX", type: "slider", model: "TRAVAUX", attrs: { step: 0.01, required: true } ,'min-max':[0, 3000000]},
    { label: "Frais d'assurance", id: "ASSU", type: "pourcentage", model: "ASSU", attrs: { step: 0.01, required: true } },
    { label: "Durée de votre prêt", id: "N", type: "slider", model: "N", attrs: { min: 1, required: true }, 'min-max':[0, 30]},
    { label: "Apport", id: "apport", type: "slider", model: "apport", attrs: { step: 0.01, required: true }, 'min-max':[0, 3000000] },
    { label: "Frais de notaire", id: "fraisNotaire", type: "pourcentage", model: "fraisNotaire", attrs: { step: 0.01, required: true } },
    { label: "Taux d'intérêt", id: "T", type: "pourcentage", model: "T", attrs: { step: 0.01, required: true } },
    { label: "Taux d'assurance", id: "ASSU", type: "pourcentage", model: "ASSU", attrs: { step: 0.01, required: true } },
    { label: "Revalorisation du bien", id: "revalorisationBien", type: "pourcentage", model: "revalorisationBien", attrs: { step: 0.01, required: true } },
    { label: "Date", id: "Date", type: "date", model: "Date", attrs: { required: true } },
]

async function handleSimulation() {
    loading.value = true

    try {
        const response = await axios.post('http://localhost:8000/api/v1/simulations/simulate', form, {
        headers: { Authorization: `Bearer ${auth.token}` }
        })
        result.value = response.data
        pop_up('Simulation réussie:', 'success')
    } catch (e) {
        pop_up('Erreur lors de la simulation.')
    } finally {
        loading.value = false
    }
}

const CalendarOn = ref(false)

watch(date, (newValue) => {
    if (newValue) {
        form.mois = String(newValue.getMonth() + 1).padStart(2, '0')
        form.annee = String(newValue.getFullYear())
    }
})


const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1);

const disabledDates = ref([{ start: null , end: yesterday }]);

const saveInUser = ref(false)

const toggleSaveInUser = () => {
    saveInUser.value = !saveInUser.value
}

const clients = ref([])

const getClients = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/v1/clients/', {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Clients récupérés:', response.data)
        clients.value = response.data 
    } catch (err) {
        pop_up('Erreur lors de la récupération des clients.')
        console.error('Erreur lors de la récupération des clients:', err)
    }
}

onMounted(() => {
    getClients()
})

const selectedClientId = ref(null)

function selectClient(id) {
    selectedClientId.value = id
}

watch(selectedClientId, (newValue) => {
    if (newValue) {
        console.log('Client sélectionné:', newValue)
    }
})

const saveSimulation = async () => {
    if (!selectedClientId.value) {
        pop_up("Veuillez sélectionner un client avant de sauvegarder la simulation.")
        return
    }

    if (!result.value) {
        pop_up("Aucune simulation à sauvegarder. Veuillez d'abord effectuer une simulation.")
        return 
    }

    try {
        const response = await axios.post('http://localhost:8000/api/v1/simulations/save-to-client', {
            simulation_data: result.value.simulation_data, 
            result: result.value.result, 
            client_id: selectedClientId.value
        }, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        console.log('Simulation sauvegardée:', response.data)
        
        saveInUser.value = false
        selectedClientId.value = null

        toggleSaveUserDisplay()
        pop_up('Simulation sauvegardée avec succès!', 'success')
    } catch (err) {
        pop_up('Erreur lors de la sauvegarde de la simulation.')
        console.error('Erreur sauvegarde:', err)
    }
}

const toggleSaveUserDisplay = () => {
    saveInUser.value = false
    selectedClientId.value = null
}

function handleClickOutside(event) {
    if (panelRef.value && !panelRef.value.contains(event.target)) {
        toggleSaveUserDisplay()
    }
}

</script>

<template>
    <div class="flex flex-wrap w-full h-full items-center justify-center gap-8">
        <div class="flex flex-col items-center justify-center gap-4 w-[32rem]">
            <form @submit.prevent="handleSimulation" class="flex flex-col w-full gap-6 border min-w-fit max-w-1/4 border-simuiolet-100/30 rounded-sm shadow-sm p-8">
                <h1 class=" text-2xl text-center font-light text-simuiolet-400">Achat en résidence principale dans l'ancien</h1>
                <Separator />
                <div v-for="field in fields" :key="field.id">
                    <hr v-if="field.type === 'categorie'">
                    <div v-if="field.type === 'slider'">
                        <label  :for="field.id">{{ field.label }} :</label><br>
                        <div class="flex w-full place-content-between items-center">
                            <input
                                :type="field.type"
                                :id="field.id"
                                :name="field.id"
                                v-model.number="form[field.model]"
                                v-bind="field.attrs"
                                class="w-full bg-transparent placeholder:text-simuiolet-400 focus:text-simuiolet-600 text-slate-700 text-sm border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simuiolet-200 hover:border-simuiolet-100 shadow-sm focus:shadow"
                            />
                        </div>
                    </div>
                    <div v-if="field.type === 'pourcentage'" class="flex gap-2 w-full place-content-between">
                        <label  :for="field.id">{{ field.label }}</label><br>
                        <input
                            :type="field.type"
                            :id="field.id"
                            :name="field.id"
                            v-model.number="form[field.model]"
                            v-bind="field.attrs"
                            class="w-1/2 border-transparent border-b-1 border-b-slate-200 text-center text-slate-700 placeholder:text-simuiolet-400 focus:text-simuiolet-600 focus:border-simuiolet-200 focus:outline-none focus:ring-0"
                        />
                        <span>%</span>
                    </div>
                    <div v-if="field.type === 'date'" class="flex flex-col items-center justify-center">
                        <button
                            type="button"
                            @click="CalendarOn = !CalendarOn"
                            class="flex items-center justify-center w-full bg-transparent placeholder:text-simuiolet-400 focus:text-simuiolet-600 text-slate-700 text-sm border border-slate-200 rounded-md px-3 py-1.5 transition duration-300 ease focus:outline-none focus:border-simuiolet-200 hover:border-simuiolet-100 shadow-sm focus:shadow"
                        >
                            <span class="flex items-center justify-center w-full">{{ moisEnLettres[date.getMonth() + 1] + ' ' + String(date.getFullYear()) }}</span>
                            <img :src="Calendar" class="w-8" alt="Calendar" />
                        </button>
                        
                        
                        <div class="relative w-full flex justify-end">
                            <Transition
                            enter-active-class="transition-all duration-300 ease-out"
                            enter-from-class="transform -translate-y-4 opacity-0"
                            enter-to-class="transform translate-y-0 opacity-100"
                            leave-active-class="transition-all duration-200 ease-in"
                            leave-from-class="transform translate-y-0 opacity-100"
                            leave-to-class="transform -translate-y-4 opacity-0"
                            >
                            <div class="absolute w-full" v-if="CalendarOn">
                                <VDatePicker
                                    :disabled-dates="disabledDates"
                                    color="simuiolet-calendar"
                                    v-model="date"
                                    mode="date"
                                    class="mt-2"
                                    expanded
                                />
                            </div>
                        </Transition>
                        </div>
                    </div>
                </div>
                
                <button class="rounded-md bg-simuiolet-600 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg focus:bg-simuiolet-400 focus:shadow-none active:bg-slate-700 hover:bg-simuiolet-400 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="submit" :disabled="loading">
                    {{ loading ? "Simulation en cours..." : "Simuler" }}
                </button>
            </form>
        </div>
        <div class="flex flex-col justify-center items-center w-[32rem] gap-4 border border-simuiolet-100/30 rounded-sm shadow-sm p-8">
            <h1 class="text-2xl font-light text-center text-simuiolet-400">Résultat de la simulation</h1>
            <Separator />
            
            <div class="flex flex-col items-center justify-center gap-2">
                <h1 class="text-lg text-center">Votre mensualité sera de :</h1>
                <p class="bg-slate-100 px-4 py-2 w-fit rounded-full text-center text-base font-medium">
                    {{ format(result?.result?.mensualite) }} €
                </p>
            </div>

            <div v-if="result" class="flex flex-col gap-2 text-sm">
                <ResultItem label="Prix du bien" :value="result?.simulation_data?.C2" />
                <ResultItem label="Frais de notaire" :value="result?.result?.fraisNotaire" />
                <ResultItem label="Garantie bancaire" :value="result?.result?.garantieBancaire" />
                <ResultItem label="Travaux" :value="result?.simulation_data?.TRAVAUX" />
                <ResultItem label="Frais d'agence" :value="result?.result?.output2?.[0]?.['Frais d\'agence']" />
                <ResultItem label="Total à financer" :value="result?.result?.output3?.[0]?.['Montant du prêt total']" />
                <ResultItem label="Revenu acquéreur minimum mensuel" :value="result?.result?.salaireMinimum" :border="false" />
            </div>  

            <div v-else class="text-gray-500 text-center italic">
                Aucune simulation n'a encore été effectuée.
            </div>

            <div v-if="result" class="flex flex-col gap-2 text-sm">
                <button @click="toggleSaveInUser()" class="rounded-md bg-simuiolet-600 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg focus:bg-simuiolet-400 focus:shadow-none active:bg-slate-700 hover:bg-simuiolet-400 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none">
                    Enregistrer la simulation
                </button>
            </div>

            <div v-if="saveInUser === true" class="fixed inset-0 bg-black/10 backdrop-blur-sm z-50 flex items-center justify-center" @click="handleClickOutside">
                <div class="flex flex-col bg-white p-6 rounded shadow-md w-full max-w-md gap-8" ref="panelRef">
                    <h1 class="text-2xl font-light">Sélectionner un client</h1>
                    
                    <div class="flex flex-col justify-between items-center mt-8">
                        <div v-if="clients.clients && clients.clients.length > 0" class="flex flex-col h-64 overflow-y-scroll gap-2 w-full">
                            <button
                                v-for="client in clients.clients"
                                :key="client.id"
                                @click="selectClient(client.id)"
                                :class="[
                                    'px-4 py-2 rounded border transition',
                                    selectedClientId === client.id
                                    ? 'bg-simuiolet-400 text-white border-simuiolet-700'
                                    : 'bg-white text-black border-gray-300 hover:bg-gray-100'
                                ]"
                            >
                                {{ client.name }}
                                <div class="text-xs opacity-75">{{ client.email }}</div>
                            </button>
                        </div>
                        
                        <div v-else class="flex flex-col items-center gap-4 p-4">
                            <p class="text-gray-500 text-center">Aucun client disponible.</p>
                            <p class="text-sm text-gray-400 text-center">Créez d'abord un client pour pouvoir sauvegarder vos simulations.</p>
                        </div>
                        
                        <div class="flex gap-4 mt-4">
                            <button 
                                @click="saveSimulation()" 
                                :disabled="!selectedClientId"
                                type="submit" 
                                class="rounded-md bg-simuiolet-600 py-2 px-4 border border-transparent text-center text-sm text-white transition-all shadow-md hover:shadow-lg focus:bg-simuiolet-400 focus:shadow-none active:bg-slate-700 hover:bg-simuiolet-400 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                            >
                                Enregistrer dans le client
                            </button>
                            <button 
                                type="button" 
                                @click="toggleSaveUserDisplay()" 
                                class="rounded-md border border-transparent py-2 px-4 text-center text-sm transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                            >
                                Retour
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>