import { ref } from 'vue'

export const pop_up_content = ref([])

let idCounter = 0

export const pop_up = (msg, type = 'error') => {
    const id = idCounter++
    pop_up_content.value.push({ id, msg, type })

    setTimeout(() => {
        pop_up_content.value = pop_up_content.value.filter(p => p.id !== id)
    }, 3000)
}
