<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'
    import axios from 'axios'

    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const auth = useAuthStore()
</script>

<template>
    <div class="flex items-center justify-center w-full flex-1">
        <h1>Homepage</h1>
    </div>
</template>