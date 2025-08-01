import { ref } from 'vue'

const placement = ref([])

function initPlacement() {
    import('@/components/Welcome.vue').then(m => {
        const Welcome = m.default
    import('@/components/LoginForm.vue').then(n => {
        const LoginForm = n.default
        placement.value = [Welcome, LoginForm]
    })
    })
}

function togglePlacement() {
    const [first, second] = placement.value
    placement.value = [second, first]
}

export function usePlacement() {
    if (placement.value.length === 0) {
        initPlacement()
    }
    return {
        placement,
        togglePlacement
    }
}
