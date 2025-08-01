<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'
    import axios from 'axios'
    import DownArrow from '@/assets/icons/down-arrow.svg'
    import HomeIcon from '@/assets/icons/home.svg'
    import PeopleIcon from '@/assets/icons/people.svg'
    import SimulateIcon from '@/assets/icons/simulate.svg'

    import Home from '@/components/Home.vue'
    import Clients from '@/components/Clients.vue'
    import Simulations from '@/components/Simulation.vue'
    import LogoutIcon from '@/assets/icons/logout.svg'

    const auth = useAuthStore()
    const router = useRouter()

    const dashboard_category = ref('home')
    const burger_menu = ref(false)

    const logout = () => {
        auth.logout()
        router.push('/')
    }

    const modifyCategory = (category) => {
        dashboard_category.value = category
        console.log('Category modified to:', dashboard_category.value)
    }

    const toggleBurgerMenu = () => {
        burger_menu.value = !burger_menu.value
        console.log('Burger menu toggled:', burger_menu.value)
    }
</script>

<template>
    <div class="flex flex-col items-center justify-center w-full h-screen">
        <div class="flex w-full h-screen">
            <section class="hidden xl:flex flex-col items-center h-full w-64 shrink-0 border-r border-gray-200 shadow-sm pr-4 justify-evenly">
                <div class="flex items-center justify-center w-full h-32 p-10">
                    <img src="@/assets/icons/Simulio_logo.svg" alt="Simulio Logo" class="w-32 h-32">
                </div>
                <div class="flex flex-col items-center justify-center w-full h-16">
                    <button class="w-full rounded-r-sm border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('home')">
                        <img :src="HomeIcon" class="w-4" alt="">
                        Home
                    </button>
                </div>
                <div class="flex flex-col items-center justify-start w-full gap-2 h-1/2">
                    <button class="w-full rounded-r-sm border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('clients')">
                        <img :src="PeopleIcon" class="w-4" alt="">
                        Clients
                    </button>
                    <button class="w-full rounded-r-sm border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('simulations')">
                        <img :src="SimulateIcon" class="w-4" alt="">
                        Simulations
                    </button>
                </div>
                <button class="w-full rounded-r-sm border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-red-100 focus:bg-red-100 active:bg-red-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="logout()">
                    <img :src="LogoutIcon" class="w-4" alt="">
                    Logout
                </button>
            </section>
            <nav class="absolute w-full flex items xl:hidden z-1000">
                <button @click="toggleBurgerMenu()" class="absolute top-4 left-1/2 -translate-x-1/2 group inline-flex w-12 h-12 text-slate-800 bg-white text-center items-center justify-center rounded shadow-[0_1px_0_theme(colors.slate.950/.04),0_1px_2px_theme(colors.slate.950/.12),inset_0_-2px_0_theme(colors.slate.950/.04)] hover:shadow-[0_1px_0_theme(colors.slate.950/.04),0_4px_8px_theme(colors.slate.950/.12),inset_0_-2px_0_theme(colors.slate.950/.04)] transition" aria-pressed="false" onclick="this.setAttribute('aria-pressed', !(this.getAttribute('aria-pressed') === 'true'))">
                    <span class="sr-only">Menu</span>
                    <svg class="w-6 h-6 fill-current pointer-events-none" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                        <rect class="origin-center -translate-y-[5px] transition-all duration-300 ease-[cubic-bezier(.5,.85,.25,1.1)] group-[[aria-pressed=true]]:translate-x-0 group-[[aria-pressed=true]]:translate-y-0 group-[[aria-pressed=true]]:rotate-[315deg]" y="7" width="16" height="2" rx="1"></rect>
                        <rect class="origin-center transition-all duration-300 ease-[cubic-bezier(.5,.85,.25,1.8)] group-[[aria-pressed=true]]:rotate-45" y="7" width="16" height="2" rx="1"></rect>
                        <rect class="origin-center translate-y-[5px] transition-all duration-300 ease-[cubic-bezier(.5,.85,.25,1.1)] group-[[aria-pressed=true]]:translate-y-0 group-[[aria-pressed=true]]:rotate-[135deg]" y="7" width="16" height="2" rx="1"></rect>
                    </svg>
                </button>
                <Transition
                        enter-active-class="transition-all duration-300 ease-out"
                        enter-from-class="transform -translate-y-4 opacity-0"
                        enter-to-class="transform translate-y-0 opacity-100"
                        leave-active-class="transition-all duration-200 ease-in"
                        leave-from-class="transform translate-y-0 opacity-100"
                        leave-to-class="transform -translate-y-4 opacity-0"
                        >
                        <div class="absolute top-18 left-1/2 -translate-x-1/2 bg-white/50 shadow-sm backdrop-blur-sm p-2 rounded-sm" v-if="burger_menu">
                            <button class="w-full rounded-md border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('home')">
                                <img :src="HomeIcon" class="w-4" alt="">
                                Home
                            </button>
                            <button class="w-full rounded-md border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('clients')">
                                <img :src="PeopleIcon" class="w-4" alt="">
                                Clients
                            </button>
                            <button class="w-full rounded-md border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="modifyCategory('simulations')">
                                <img :src="SimulateIcon" class="w-4" alt="">
                                Simulations
                            </button>
                            <button class="w-full rounded-md border border-transparent py-2 px-4 flex items-center gap-4 text-center text-lg transition-all text-slate-600 hover:bg-red-100 focus:bg-red-100 active:bg-red-100 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" @click="logout()">
                                <img :src="LogoutIcon" class="w-4" alt="">
                                Logout
                            </button>
                        </div>
                </Transition>
            </nav>
            <div class="flex-1 flex-col items-center justify-start overflow-auto">
                <Home v-if="dashboard_category == 'home'" />
                <Clients v-if="dashboard_category == 'clients'" :clients="clients" @get-clients="getClients" />
                <Simulations v-if="dashboard_category == 'simulations'" :clients="clients" @get-clients="getClients" />
            </div>
        </div>
    </div>
</template>
