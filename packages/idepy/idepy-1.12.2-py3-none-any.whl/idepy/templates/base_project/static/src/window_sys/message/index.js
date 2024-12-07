const {createApp, ref} = Vue

const app = createApp({
    setup() {
        const rData = ref({
            title: "",
            message: "",
        })

        return {
            rData
        }
    },

})
app.use(ElementPlus, {
    locale: ElementPlusLocaleZhCn
});
const vm = app.mount('#app')

function closeWindow() {
    pywebview.api.close()
}

async function initData() {
    const data = await pywebview.api.get_data()
    vm.rData = data ?? {}

}

window.addEventListener('pywebviewready', () => {
    initData()
})