<template>
    <div :class="['flex flex-col gap-1 justify-center', border ? 'border-b border-slate-200 pb-2' : '']">
        <p>
        <strong>{{ label }} :</strong>
        {{ formattedValue }} €
        </p>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    label: { type: String, required: true },
    value: [Number, String],
    border: { type: Boolean, default: true }
})

const formattedValue = computed(() => {
    const num = Number(props.value)
    return isNaN(num) ? '—' : num.toFixed(2)
})
</script>
