const containerUserRequest = document.querySelector(".container-request-user-credentials");
const userCredentialInputs = document.querySelectorAll(".user-credential-input");
// form elements
const togglePassword = document.querySelector('#togglePassword');
const toggleConfirmPassword = document.querySelector('#toggleConfirmPassword');

const user = document.querySelector("#user");
const password = document.querySelector('#pass');
const confirmPassword = document.querySelector('#pass-confirm');

const form = document.querySelector("#form-user-credentials");
const userIconSuccess = document.querySelector(".user-icon-success");
const passIconSuccess = document.querySelector(".pass-icon-success");
const pass2IconSuccess = document.querySelector(".pass2-icon-success");
const passFeedBack = document.querySelector(".pass-feedback");
const alertBackdrop = document.querySelector(".backdrop-alert");

const containerContent = document.querySelector(".container-content");
const containerContentHeader = document.querySelector(".container-content-header");


async function isUserSet() {
    return await eel.is_user_set()()
}

async function getScreenSize() {
    return await eel.get_screen_size()()
}

async function setUserCredentials(username, password) {
    return await eel.set_user_credential(username, password)()
}

async function getUserName() {
    return await eel.get_username()()
}

async function getData(month) {
    return await eel.get_data(month)()
};

async function createWorkDirectory(month) {
    return await eel.create_work_directory(month)()
};


const toggleInputPass = (el, inputElement) => {
    el.addEventListener('click', () => {
        const type = inputElement.getAttribute('type') === 'password' 
        ? 'text' : 'password';
        
        if (password.value && confirmPassword.value) {
            inputElement.setAttribute('type', type);
            el.classList.toggle('fa-eye-slash');
            el.classList.add('fa-eye');
        }
    });
}


form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    if(user.value.length > 0 && password.value.length > 0 
        && confirmPassword.value.length > 0 
        && password.value === confirmPassword.value) {
        
        userIconSuccess.classList.remove('d-none');
        passIconSuccess.classList.remove('d-none');
        pass2IconSuccess.classList.remove('d-none');
        togglePassword.classList.add('d-none');
        toggleConfirmPassword.classList.add('d-none');
        passFeedBack.classList.add('d-none');

        const username = user.value;
        const pass = password.value;
        
        // send to database
        setUserCredentials(username, pass).then(response => {
            
            if (response) {
                Array.prototype.slice.call(userCredentialInputs)
                    .forEach(input => input.value = "");

                document.querySelector("#user-success-inserted-alert")
                .classList.remove("d-none");
                

                setTimeout(() => {
                        containerUserRequest.classList.add("d-none");
                        containerContent.classList.remove("d-none");
                }, 3000);
                
                init();    
                
            } else {
                document.querySelector("#user-failed-insert-alert")
                    .classList.remove("d-none")
            }
        })
        
    } else {
        passIconSuccess.classList.add('d-none');
        pass2IconSuccess.classList.add('d-none');
        togglePassword.classList.remove('d-none');
        toggleConfirmPassword.classList.remove('d-none');
        passFeedBack.classList.remove('d-none');
    }
})


const getMappedObject = obj => {
    return {type, } = obj;
}


document.querySelector(".perfil").addEventListener("click", () => {
    document.querySelector(".perfil-modal-info").classList.toggle("d-none");
})


const setSelectMonths = () => {
    const {months, actualMonth} = getMonths();

    months.map(month => {
        const option = document.querySelector("#work-month-select option").cloneNode(true);
        const select = document.querySelector("#work-month-select");
        
        if (month === actualMonth) {
            option.setAttribute("selected", month);
        }
        
        option.style.display = "block";
        option.setAttribute("value", month.replace("/", "-"));
        option.textContent = month;

        select.append(option);
    })

    return actualMonth;
}

const setData = () => {
    getData(actualMonth.replace("/", "-"))
        .then(response => {

            console.log(response)

            // verificar e fazer a interação com o usuário
            if (response.data.length == 0) return;
            
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
}


const init = () => {
    const actualWorkMonth = setSelectMonths();
    
    getUserName().then(response => {
        username = response; 
        document.querySelector(".perfil .user-content #username").innerHTML = username;
    })

    createWorkDirectory(actualWorkMonth.replace("/", "-"))
        .then(response => {
            if (response === null) {
                alertBackdrop.querySelector("strong").textContent = "Verificando diretório de trabalho, aguarde...";
            }else {
                alertBackdrop.querySelector("strong").textContent = "Criando diretório de trabalho, aguarde..."
            }
            
            setTimeout(() => {
                alertBackdrop.classList.add("d-none")
                containerContentHeader.classList.remove("d-none")
            }, 2000);
            
            alertBackdrop.querySelector("strong").textContent = "Verificando diretório de trabalho, aguarde...";
        })
}


const getMonths = () => {
    const today = new Date();
    const year = today.getFullYear();
    let actualMonth = today.getMonth();
    actualMonth = actualMonth < 9 ? `0${actualMonth+1}/${year}`: `${actualMonth+1}/${year}`;

    const months = []

    for (let index = 1; index <= 12; index++) {
        months.push( index < 10 ? `0${index}/${year}`: `${index}/${year}` );
    }

    return {months, actualMonth};
}


window.onload = () => {
    isUserSet().then(response => {
        alertBackdrop.querySelector("strong").textContent = "Inicializando.."

        if(response) {
            containerContent.classList.remove("d-none");
            alertBackdrop.classList.remove("d-none");
            setTimeout(() => init(), 1000);
        }

        toggleInputPass(togglePassword, password);
        toggleInputPass(toggleConfirmPassword, confirmPassword);
        !response && containerUserRequest.classList.remove("d-none");
    })
}

// window.addEventListener('contextmenu', e => {
// 	if (e.button == 2){
// 		e.preventDefault();
// 		return false;
// 	}
// })

// window.addEventListener('keyup', e => {
// 	if (e.key === 93){
// 		e.preventDefault();
// 		return false;
// 	}
// })