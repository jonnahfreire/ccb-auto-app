async function getData(params=null) {
    const data = await eel.get_data(
        //params // Pass params to main function
        "03-2022"
    )()
    return data;
};


const getMappedObject = obj => {
    return {
    }
}


getData()
    .then(response => {
        
        const debts1000 = response["1000"]
        const debts1010 = response["1010"]
        console.log(debts1000, debts1010)

        console.log(debts1000[0]["hist-1"])

        const debts1000Length = debts1000.length
        const debts1010Length = debts1010.length
        const model1000Title = document.querySelector(".content-model .model-account-1000")
        const contentModel1000 =  document.querySelector(".content-model .d-1000")

        const model1010Title = document.querySelector(".content-model .model-account-1010")
        const contentModel1010 =  document.querySelector(".content-model .d-1010")
        
        model1000Title.textContent = "1000:"
        contentModel1000.textContent =  debts1000Length > 1 
            ? "Encontrados " + debts1000Length + " despesas."
            : "Encontrados " + debts1000Length +" despesa."

        model1010Title.textContent = "1010:"
        contentModel1010.textContent =  debts1010Length > 1 
            ? "Encontrados " + debts1010Length + " despesas."
            : "Encontrados " + debts1010Length +" despesa."
})