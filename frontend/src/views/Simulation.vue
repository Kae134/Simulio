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
    <div class="flex flex-col items-center justify-center gap-4 p-2">
        <form @submit.prevent="handleSimulation" class="flex flex-col w-full gap-4 border min-w-fit max-w-1/4 border-simuiolet-100/30 rounded-sm shadow-sm p-4">
        <h1 class=" text-2xl font-light">Achat en residence principale dans l'ancien</h1>
        <div v-for="field in fields" :key="field.id">
            <hr v-if="field.type === 'categorie'">
            <div v-if="field.type === 'slider'">
                <label  :for="field.id">{{ field.label }} :</label><br>
                <div class="flex w-full place-content-between items-center">
                    <!-- <input
                        type="range"
                        :id="field.id"
                        :name="field.id"
                        :min="field['min-max'][0]"
                        :max="field['min-max'][1]"
                        v-model.number="form[field.model]"
                        v-bind="field.attrs"
                        class="range-input"
                    /> -->
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
                    class="w-1/2 border-transparent border-b-1 border-b-slate-200 text-center text-slate-700 focus:border-simuiolet-200 focus:outline-none focus:ring-0"
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

                <VDatePicker
                v-if="CalendarOn"
                :disabled-dates="disabledDates"
                v-model="date"
                mode="date"
                />
            </div>
        </div>

        <button type="submit" :disabled="loading">
            {{ loading ? "Simulation en cours..." : "Simuler" }}
        </button>
        </form>

        <div v-if="result" style="margin-top: 2rem;">
        <h2>Résultat</h2>
        <pre>{{ result }}</pre>
        </div>

        <p v-if="error" style="color: red; margin-top: 1rem;">{{ error }}</p>
    </div>

</template>
