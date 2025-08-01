<script setup>
import { reactive, ref, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { pop_up } from '@/stores/popUpStore'

const auth = useAuthStore()
const loading = ref(false)
const result = ref(null)
const error = ref(null)

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

