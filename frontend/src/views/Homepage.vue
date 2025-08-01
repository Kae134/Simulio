<script setup>
    import CheckIcon from '@/assets/icons/check-good.svg'
    import ImageHomepage from '@/assets/images/Simulio_homepage.png'

    const data = [
        {"title":"Validez vos chiffres sans attendre un courtier", "content":"Gagnez du temps et accélérez le processus de vente."},
        {"title":"Projetez vos clients comme jamais auparavant", "content":"Rendez l'immobilier concret avec des simulations précises et visuelles."},
        {"title":"Augmentez vos revenus de 65 %", "content":"Une solution qui transforme vos prospects en clients signés."},
        {"title":"Prêt à l'usage pour un junior", "content":"Les nouveaux conseillers prennent une assise immédiate grâce à Simulio."},
    ]
</script>

<template>
    <section class="bg-white text-slate-900">
        <div class="max-w-7xl mx-auto px-6 py-20 flex flex-col-reverse md:flex-row items-center gap-12">
        <div class="md:w-1/2 text-center md:text-left">
            <h1 class="text-4xl md:text-5xl font-extrabold mb-6">
            Boostez vos <span class="text-simugreen-600">ventes immobilières</span><br />
            Grâce aux simulateurs les plus puissants du marché
            </h1>
            <p class="text-lg text-slate-600 mb-8">
            Simulio vous aide à convaincre plus de clients grâce à des simulations de prêt claires, rapides et précises.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <a href="https://fssnjvuzk2w.typeform.com/to/ZaGUtE48" class="flex items-center justify-center rounded-md bg-simugreen-500 py-2 px-4 h-16 w-64 border border-transparent text-center text-lg text-white transition-all shadow-md hover:shadow-lg hover:bg-simugreen-400">
                Réservez votre démo aujourd'hui
            </a>
            <a href="https://calendly.com/simulio/20min" class="flex items-center justify-center text-center py-2 px-4 h-16 w-64 bg-transparent placeholder:text-simugreen-400 focus:text-simugreen-600 text-slate-700 text-lg border border-slate-200 rounded-md transition duration-300 ease focus:outline-none focus:border-simugreen-200 hover:border-simugreen-100 shadow-sm focus:shadow">
                Prendre RDV
            </a>
            </div>
        </div>

        <div class="md:w-1/2">
            <img
            src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c"
            alt="Simulation immobilière"
            class="rounded-2xl shadow-lg"
            />
        </div>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-8 py-16 p-16">
            <div class="flex flex-col items-center justify-center min-w-132 gap-8">
                <div class="flex items-center justify-center w-fit gap-8" v-for="item in data">
                    <img :src="CheckIcon" class="w-12 p-2 bg-simugreen-100/50 rounded-full" alt="">
                    <div class="flex flex-col w-128">
                        <h3 class="text-xl text-slate-800 font-semibold mb-2">{{ item.title }}</h3>
                        <p class="text-slate-600 font-light">{{ item.content }}</p>
                    </div>
                </div>
            </div>
            <img class="rounded-sm shadow-lg" :src="ImageHomepage" alt="">
        </div>
    </section>
</template>