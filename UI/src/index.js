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
const content = document.querySelector(".container-content .content");

const timeout = 2000;

async function getFolderPath() {
    return await eel.get_folder_path()()
}

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

async function eelAlert(title, message) {
    return await eel.alert(title, message)()
};

async function getMonthDirectoryList() {
    return await eel.get_month_directory_list()()
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
                }, timeout);
                
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

    return {
        "type":obj["type"],
        "num":obj["num"],
        "date":obj["date"],
        "value":obj["value"],
        "emitter":obj["emitter"],
        "expenditure":obj["expenditure"],
        "checkNum":obj["check-num"],
        "docNum":obj["doc-num"],
        "fileName":obj["file-name"],
        "costCenter":obj["cost-center"],
        "costAccount":obj["cost-account"],
        "paymentForm":obj["payment-form"],
        "hist1":obj["hist-1"],
        "hist2":obj["hist-2"]
    };
}


document.querySelector(".perfil").addEventListener("click", () => {
    document.querySelector(".perfil-modal-info").classList.toggle("d-none");
})

document.querySelector(".btn-create").addEventListener("click", () => {

    const modalSelectBackdrop = document.querySelector(".select-month-modal-backdrop")
    modalSelectBackdrop.classList.remove("d-none");

    let selectedMonth = null;

    document.querySelector("#work-month-select").addEventListener('change', (e) => {
        selectedMonth = e.target.value;
    })

    
    document.querySelector(".select-month-modal-backdrop .btn-ok").addEventListener("click", () => {
        modalSelectBackdrop.classList.add("d-none")   
        
        console.log(selectedMonth)
        createWorkDirectory(selectedMonth)
            .then(response => response && init())
    })
})

document.querySelector(".btn-add").addEventListener("click", () => {

    getFolderPath().then(response => {

        if (response) {
            console.log(response)
        }
        // document.querySelector(".perfil-modal-info").classList.toggle("d-none");

    })
})


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

const fillContent = (debtList, account) => {
    const contentMessage1000 = document.querySelector(".account1000-content .message");
    const contentMessage1010 = document.querySelector(".account1010-content .message");
    const content1000Info =  document.querySelector(".account1000-content");
    const content1010Info =  document.querySelector(".account1010-content");

    console.log(debtList, account)

    if(debtList.length > 0) {
        // clear content
        account === "1000" && document.querySelectorAll(".account1000-content .model-item")
            .forEach(item => item.remove());
        
        account === "1010" && document.querySelectorAll(".account1010-content .model-item")
            .forEach(item => item.remove());

        debtList.forEach(debt => {
            const model = document.querySelector(".content-model .debt-info").cloneNode(true);

            model.querySelector(".filetype").textContent = debt.type.replace("NOTA FISCAL", "NF");
            model.querySelector(".filenumber").textContent =  debt.num;
            model.querySelector(".filedate").textContent =  `${debt.date[0]}/${debt.date[1]}/${debt.date[2]}`;
            model.querySelector(".filevalue").textContent = "R$ " + debt.value;

            account === "1000" && contentMessage1000.classList.add("d-none");
            account === "1010" && contentMessage1010.classList.add("d-none");
            
            account === "1000" && content1000Info.append(model);
            account === "1010" && content1010Info.append(model);
        })
    }
}


const setData = (month) => {
    getData(month)
        .then(response => {
            console.log(response)

            if (response["1000"].length == 0 && response["1010"].length == 0) return;

            const debts1000 = response["1000"].map(debt => getMappedObject(debt));
            const debts1010 = response["1010"].map(debt => getMappedObject(debt));


            fillContent(debts1000, "1000");
            fillContent(debts1010, "1010");
    })
}


const init = () => {
    const actualWorkMonth = setSelectMonths().replace("/", "-");
    document.querySelector(".container-content .actual-month span").textContent = actualWorkMonth.replace("-", "/");
    
    getUserName().then(response => {
        username = response; 
        document.querySelector(".perfil .user-content #username").innerHTML = username;
    })

    createWorkDirectory(actualWorkMonth)
        .then(response => {
            if (response === null) {
                alertBackdrop.querySelector("strong").textContent = "Verificando diretório de trabalho, aguarde...";
            }else {
                alertBackdrop.querySelector("strong").textContent = "Criando diretório de trabalho, aguarde..."
            }
            
            setTimeout(() => {
                alertBackdrop.classList.add("d-none")
                containerContentHeader.classList.remove("d-none")
                content.classList.remove("d-none")
            }, timeout); // 2000
            
            alertBackdrop.querySelector("strong").textContent = "Verificando diretório de trabalho, aguarde...";
        })
    
    getMonthDirectoryList().then(response => {
        if (response.length > 0) {
            const directoryContainer = document.querySelector(".month-directories");

            document.querySelectorAll(".month-directories .work-month-directory")
                .forEach(item => item.remove());
            
            response.forEach(month => {

                const directoryModel = document.querySelector(".content-model .work-month-directory").cloneNode(true);

                directoryModel.querySelector(".folder-title").textContent = month.replace("-", "/");
                directoryContainer.append(directoryModel);

                if (month === actualWorkMonth) {
                    directoryModel.classList.add("work-month-directory-selected");
                    directoryModel.querySelector(".bi-folder").classList.add("d-none");
                    directoryModel.querySelector(".bi-folder2-open").classList.remove("d-none");
                }

                directoryModel.addEventListener("click", () => {
                    directoryContainer.querySelectorAll(".work-month-directory-selected")
                        .forEach(dir => {
                            dir.classList.contains("work-month-directory-selected")
                                && dir.classList.remove("work-month-directory-selected");
                            
                            dir.querySelector(".bi-folder").classList.remove("d-none");
                            dir.querySelector(".bi-folder2-open").classList.add("d-none");
                        });

                    if (directoryModel.classList.contains("work-month-directory-selected")){
                        return false;
                    }
                    
                    if (!directoryModel.classList.contains("work-month-directory-selected")){
                        directoryModel.classList.add("work-month-directory-selected");
                        directoryModel.querySelector(".bi-folder").classList.toggle("d-none");
                        directoryModel.querySelector(".bi-folder2-open").classList.toggle("d-none");
                    }

                    setData(month);
                })
            })
        }
    })
    
    setData(actualWorkMonth);
}

window.onload = () => {
    isUserSet().then(response => {
        alertBackdrop.querySelector("strong").textContent = "Inicializando.."

        if(response) {
            containerContent.classList.remove("d-none");
            alertBackdrop.classList.remove("d-none");
            setTimeout(() => init(), timeout); //1000
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