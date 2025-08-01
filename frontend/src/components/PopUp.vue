<script setup>
import { pop_up_content } from '@/stores/popUpStore';
import errorIcon from '@/assets/icons/error.svg';
import successIcon from '@/assets/icons/success.svg';
import warningIcon from '@/assets/icons/warning.svg';
</script>

<template>
    <div class="fixed bottom-4 left-1/2 -translate-x-1/2 flex flex-col gap-2 items-center z-50">
        <transition-group name="slide-up" tag="div">
            <div
                v-for="popup in pop_up_content"
                :key="popup.id"
                class="min-w-24 max-w-128 px-4 py-2 h-12 mb-2 bg-black/80 backdrop-blur-sm flex items-center justify-center rounded-sm shadow gap-4"
                :class="{
                'text-red-300': popup.type === 'error',
                'text-green-300': popup.type === 'success',
                'text-yellow-300': popup.type === 'warning'
                }"
            >
                <img v-if="popup.type === 'error'" :src="errorIcon" alt="" class="w-6 h-6">
                <img v-if="popup.type === 'success'" :src="successIcon" alt="" class="w-6 h-6">
                <img v-if="popup.type === 'warning'" :src="warningIcon" alt="" class="w-6 h-6">
                {{ popup.msg }}
            </div>
        </transition-group>
    </div>
</template>
