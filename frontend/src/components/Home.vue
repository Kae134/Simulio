<script setup>
import { reactive, ref, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import Calendar from '@/assets/icons/calendar.svg'

const auth = useAuthStore()
const loading = ref(false)
const result = ref(null)
const error = ref(null)

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
    { label: "Frais d'assurance (%)", id: "ASSU", type: "pourcentage", model: "ASSU", attrs: { step: 0.01, required: true } },
    { label: "Durée de votre pret", id: "N", type: "slider", model: "N", attrs: { min: 1, required: true }, 'min-max':[0, 30]},
    { label: "Apport", id: "apport", type: "slider", model: "apport", attrs: { step: 0.01, required: true }, 'min-max':[0, 3000000] },
    { label: "Frais de notaire (%)", id: "fraisNotaire", type: "pourcentage", model: "fraisNotaire", attrs: { step: 0.01, required: true } },
    { label: "Taux d'intérêt (%)", id: "T", type: "pourcentage", model: "T", attrs: { step: 0.01, required: true } },
    { label: "Taux d'assurance (%)", id: "ASSU", type: "pourcentage", model: "ASSU", attrs: { step: 0.01, required: true } },
    { label: "Revalorisation du bien", id: "revalorisationBien", type: "pourcentage", model: "revalorisationBien", attrs: { step: 0.01, required: true } },
    { label: "Date", id: "Date", type: "date", model: "Date", attrs: { required: true } },
]

async function handleSimulation() {
    loading.value = true
    result.value = null
    error.value = null

    try {
        const response = await axios.post('http://localhost:8000/api/v1/simulations/simulate', form, {
        headers: { Authorization: `Bearer ${auth.token}` }
        })
        result.value = response.data
    } catch (e) {
        error.value = 'Erreur lors de la simulation.'
    } finally {
        loading.value = false
    }
}

const CalendarOn = ref(true)

watch(date, (newValue) => {
    if (newValue) {
        form.mois = String(newValue.getMonth() + 1).padStart(2, '0')
        form.annee = String(newValue.getFullYear())
    }
})


const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1);

const disabledDates = ref([{ start: null , end: yesterday }]);
</script>

<template>
    <div class="flex flex-col items-center justify-center w-full h-full gap-4 p-4">
        <div class="text-4xl animate-wave">👋</div>
        <h1 class="text-2xl font-bold text-center">
        Bienvenue sur le tableau de bord
        </h1>
        <p class="flex flex-col items-center text-gray-600 text-center">
            Utilisez le menu à gauche pour naviguer entre les sections :
        </p>
        <ul class="list-disc list-inside text-left text-gray-600">
            <li>clients</li>
            <li>simulations</li>
            <li>et plus encore</li>
        </ul>
    </div>
</template>

