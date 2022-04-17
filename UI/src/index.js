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
const folderContextMenu = document.querySelector(".folder-context-menu");
const contextMenuCurrentFolder = {"element": "", "title": ""};
const timeout = 100;
const system = {"running": false};

async function getFilesFromFolder() {
    return await eel.get_files_from_folder()()
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

async function getStatus() {
    return await eel.get_current_status()()
}

async function getSysPath() {
    return await eel.get_sys_path()()
}

async function openDirectory(path) {
    return await eel.open_directory(path)()
}

async function getData(month) {
    return await eel.get_data(month)()
};

async function createWorkDirectory(month) {
    return await eel.create_work_directory(month)()
};

async function insertDebt(month, workMonthPath, debtList, window=false) {
    return await eel.insert_new_debt(month,workMonthPath, debtList, window)()
};

async function getWorkMonthPath(month) {
    return await eel.get_work_month_path(month)()
};

async function eelAlert(title, message) {
    return await eel.alert(title, message)()
};

async function getMonthDirectoryList() {
    return await eel.get_month_directory_list()()
};

async function removeMonthDirectory(dirname) {
    return await eel.remove_month_directory(dirname)()
};

async function removeCurrentUser() {
    return await eel.remove_current_user()()
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

// Set user
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
                    splashScreen.show();
                }, timeout);
                        
                setTimeout(() => { 
                    containerContent.classList.remove("d-none");
                    splashScreen.dismiss();
                    init();
                }, timeout);
                
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
        "hist2":obj["hist-2"],
        "fileType":obj["file-type"],
    };
}

// perfil
document.querySelector(".perfil").addEventListener("click", () => {
    document.querySelector(".perfil-modal-info").classList.toggle("d-none");
    document.querySelector(".perfil-modal-info").classList.add("p-m-opacity");
})

// Remove user
document.querySelector(".perfil-modal-info .remove-user").addEventListener("click", () => {
    const removeUserBackdrop = document.querySelector(".remove-user-modal-backdrop");
    removeUserBackdrop.classList.remove("d-none");
    
    const removeUserModal = document.querySelector(".modal-remove-user");
    
    const btnClose = removeUserModal.querySelector("svg");
    const btnOk = removeUserModal.querySelector(".modal-remove-user-footer .btn-ok");
    const btnCancel = removeUserModal.querySelector(".btn-cancel");
    

    btnClose.addEventListener("click",
        () => removeUserBackdrop.classList.add("d-none"));
    
    btnCancel.addEventListener("click",
        () => removeUserBackdrop.classList.add("d-none"));
    
    btnOk.addEventListener("click", () => {
        removeCurrentUser().then(response => {
            response && window.location.reload();
        })
    });
})

// Settings
document.querySelector(".perfil-modal-info .settings").addEventListener("click", () => {
    const content = document.querySelector(".content")
    const settingsContainer = document.querySelector(".container-settings")
    content.classList.add("d-none");
    settingsContainer.classList.remove("d-none");

    document.querySelector(".container-settings .btn-go-back")
        .addEventListener("click", () => {
            settingsContainer.classList.add("d-none");
            content.classList.remove("d-none");
        })
})

// Perfil modal
document.querySelector(".container-settings").addEventListener("click", () => {
    document.querySelector(".perfil-modal-info").classList.add("d-none");
    document.querySelector(".perfil-modal-info").classList.remove("p-m-opacity");
})

document.querySelector(".content").addEventListener("click", () => {
    document.querySelector(".perfil-modal-info").classList.add("d-none");
    document.querySelector(".perfil-modal-info").classList.remove("p-m-opacity");
})

document.querySelector("body").addEventListener("click", () => {
    folderContextMenu.classList.add("d-none");
    folderContextMenu.classList.remove("f-c-opacity");
})

document.querySelector(".btn-create").addEventListener("click", () => {
    const modalSelectBackdrop = document.querySelector(".select-month-modal-backdrop");
    const modalSelectCloseBtn = document.querySelector(".modal-select-month svg");
    modalSelectBackdrop.classList.remove("d-none");

    let selectedMonth = null;
    modalSelectCloseBtn.addEventListener("click", () => {
        modalSelectBackdrop.classList.add("d-none");
    })

    document.querySelector("#work-month-select").addEventListener('change', (e) => {
        selectedMonth = e.target.value;
    })

    modalSelectBackdrop.querySelector(".btn-ok")
        .addEventListener("click", () => {
        modalSelectBackdrop.classList.add("d-none")   
        
        selectedMonth && createWorkDirectory(selectedMonth)
            .then(response => response && init())
    })
})

document.querySelector(".btn-add").addEventListener("click", () => {
    getFilesFromFolder().then(response => response && init())
})

// Automation Start
document.querySelector(".btn-start").addEventListener("click", async() => {
    const monthDirectories = document
        .querySelectorAll(".month-directories .work-month-directory");
        
    const selectedMonthDir = [...monthDirectories].filter(month => {
            if (month.classList.contains("work-month-directory-selected")){
                return month
            }
        })[0];

    const selectedMonth = selectedMonthDir.querySelector(".folder-title").textContent;
    
    const workMonthPath = await getWorkMonthPath(selectedMonth);
    
    getData(selectedMonth.replace("/", "-"))
        .then(response => {
            const debts1000 = response["1000"]
            const debts1010 = response["1010"]

            const allDebts = [...debts1000, ...debts1010];
            
            const items = [...document.querySelectorAll(".debt-info")];
            const files = {"success": [], "error": []};

            if (debts1000 || debts1010){
                insertDebt(selectedMonth, workMonthPath, allDebts)
                    .then(response => {
                        files.success = response.success;
                        files.error = response.error;
                    });

                system.running = true;

                const statusCheck = setInterval(() => {
                    getStatus().then(response => {

                        const current = items.filter(item => 
                            (item.querySelector(".filename")
                                .textContent.trim() === response.current["file-name"]))[0]

                        if (response.started && !response.finished_all){
                            if (!document.querySelector(".status-container .not-started").classList.contains("d-none")) {
                                document.querySelector(".status-container .not-started").classList.add("d-none");
                                document.querySelector(".status-container .started").classList.remove("d-none");   
                            }
                            
                            if (!current.querySelector(".not-started").classList.contains("d-none")) {
                                current.querySelector(".not-started").classList.add("d-none");
                                current.querySelector(".started").classList.remove("d-none");    
                            }

                            if (current.querySelector(".started").classList.contains("d-none")) {
                                current.querySelector(".started").classList.remove("d-none"); 
                            }
                        }
                        
                        if (response.started && response.finished) {
                            items[items.indexOf(current) - 1]
                                .querySelector(".started").classList.add("d-none");

                            items[items.indexOf(current) - 1]
                                .querySelector(".finished").classList.remove("d-none");
                            
                            if (current.querySelector(".started").classList.contains("d-none")) {
                                current.querySelector(".started").classList.add("d-none"); 
                                current.querySelector(".finished").classList.remove("d-none");
                            }
                        }

                        if (response.finished_all) {
                            current.querySelector(".started").classList.add("d-none"); 
                            current.querySelector(".finished").classList.remove("d-none");

                            document.querySelector(".status-container .started").classList.add("d-none");
                            document.querySelector(".status-container .finished").classList.remove("d-none");
                            clearInterval(statusCheck);
                        }                        
                    })
                }, 500);
            }
    })
})
// End Automation


const getMonths = () => {
    const today = new Date();
    const year = today.getFullYear();
    let actualMonth = today.getMonth();
    actualMonth = actualMonth < 9 ? `0${actualMonth+1}/${year}`: `${actualMonth+1}/${year}`;

    const months = []

    for (let index = 1; index <= 12; index++) {
        months.push( index < 10 ? `0${index}/${year}`: `${index}/${year}` );
    }

    actualMonth = actualMonth.toString()
    return {months, actualMonth};
}


const setSelectMonths = () => {
    const {months, actualMonth} = getMonths();

    const options = document.querySelectorAll("#work-month-select option");
    if (options.length == 14) return actualMonth;

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

function getPosition(el) {
    let xPos = 0;
    let yPos = 0;
   
    while (el) {
        if (el.tagName == "BODY") {
            let xScroll = el.scrollLeft || document.documentElement.scrollLeft;
            let yScroll = el.scrollTop || document.documentElement.scrollTop;
   
            xPos += (el.offsetLeft - xScroll + el.clientLeft);
            yPos += (el.offsetTop - yScroll + el.clientTop);

        } else {
            xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
            yPos += (el.offsetTop - el.scrollTop + el.clientTop);
        }
   
        el = el.offsetParent;
    }

    return {
        x: xPos,
        y: yPos
    };
}

const fillContent = (debtList, account) => {
    const contentMessage1000 = document.querySelector(".account1000-content .message");
    const contentMessage1010 = document.querySelector(".account1010-content .message");
    const content1000Info =  document.querySelector(".account1000-content");
    const content1010Info =  document.querySelector(".account1010-content");

    // clear content
    account == "1000" && content1000Info.querySelectorAll(".model-item")
        .forEach(item => item.remove());
    
    account == "1010" && content1010Info.querySelectorAll(".model-item")
        .forEach(item => item.remove());
        
    if(debtList.length > 0) {
        debtList.forEach(debt => {
            const debtValue = new Intl.NumberFormat(`pt-BR`, {
                currency: `BRL`,
                style: 'currency',
            }).format(debt.value.replace(",","."));

            const model = document.querySelector(".content-model .debt-info").cloneNode(true);
            
            if (debt.fileType === "pdf") {
                model.querySelector(".filetype svg.pdf").classList.remove("d-none");

            } else if (debt.fileType === "jpg" || debt.fileType === "jpeg") {
                model.querySelector(".filetype svg.jpg").classList.remove("d-none");

            }else if (debt.fileType === "png") {
                model.querySelector(".filetype svg.png").classList.remove("d-none");
            }

            if (debt.fileName.includes("DB AT")) {
                let fileName = debt.fileName.replace("DB AT", "");
                fileName = fileName.length > 12 ? `${fileName.slice(0, 12)}...`: fileName;
                model.querySelector(".filename").textContent = fileName;

            } else {
                model.querySelector(".filename").textContent = debt.fileName;
            }
            model.querySelector(".filedate").textContent =  `${debt.date[0]}/${debt.date[1]}/${debt.date[2]}`;
            model.querySelector(".filevalue").textContent = debtValue;
            model.querySelector(".filedebttype").textContent = "DP " + debt.expenditure;
                
            account === "1000" && contentMessage1000.classList.add("d-none");
            account === "1010" && contentMessage1010.classList.add("d-none");
            
            account === "1000" && content1000Info.append(model);
            account === "1010" && content1010Info.append(model);
        })
    } else {
        account === "1000" && contentMessage1000.classList.remove("d-none");
        account === "1010" && contentMessage1010.classList.remove("d-none");
    }
}


const setData = (month) => {
    getData(month)
        .then(response => {
            const debts1000 = response["1000"].map(debt => getMappedObject(debt));
            const debts1010 = response["1010"].map(debt => getMappedObject(debt));

            if (debts1000.length > 0 || debts1010.length > 0) {
                document.querySelector(".status-container").classList.remove("d-none");
            } else {
                document.querySelector(".status-container").classList.add("d-none");
            }

            fillContent(debts1000, "1000");
            fillContent(debts1010, "1010");
    })
}

folderContextMenu.querySelector(".remove-folder").addEventListener("click", () => {
    const modalRemoveMonthBackDrop = document.querySelector(".remove-month-modal-backdrop");
    modalRemoveMonthBackDrop.classList.remove("d-none");

    const modalRemoveMonthBtnOk = document.querySelector(".modal-remove-footer .btn-ok");
    const modalRemoveMonthClose = document.querySelector(".modal-remove-header svg");
    const modalRemoveMonthBtnCancel = document.querySelector(".modal-remove-footer .btn-cancel");

    modalRemoveMonthClose.addEventListener("click", () => {
        modalRemoveMonthBackDrop.classList.add("d-none");
    })

    modalRemoveMonthBtnCancel.addEventListener("click", () => {
        modalRemoveMonthBackDrop.classList.add("d-none");
    })

    modalRemoveMonthBtnOk.addEventListener("click", () => {
        modalRemoveMonthBackDrop.classList.add("d-none");
        removeMonthDirectory(contextMenuCurrentFolder.title)
            .then(response => {
                response && init();
            })
    })
})

folderContextMenu.querySelector(".open-folder").addEventListener("click", () => {
    getSysPath().then(path => {
        const folderPath = path+"/"+contextMenuCurrentFolder.title
        path && openDirectory(folderPath).then();
    })
})

const showFolderContextMenu = (element) => {
    const windowRightCorner = window.innerWidth;
    const position = getPosition(element)
    
    const elementRight = element.getBoundingClientRect().right;
    const elementLeft = element.getBoundingClientRect().left;
   
    folderContextMenu.classList.remove("d-none");
    folderContextMenu.style.opacity = 1;

    if (elementRight >= windowRightCorner){
        folderContextMenu.style.left = 
            windowRightCorner - folderContextMenu
                                .getBoundingClientRect()
                                .width - 20 + "px";

    } else if (elementLeft <= 0){
        folderContextMenu.style.left = 20 + "px";

    } else {
        folderContextMenu.style.left = elementLeft + "px";
    }
    folderContextMenu.style.top = position.y + 60 + "px";
}

const init = () => {
    const actualWorkMonth = setSelectMonths().replace("/", "-");

    document.querySelector(".container-content .actual-month span")
        .textContent = actualWorkMonth.replace("-", "/");
    
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

            directoryContainer.querySelectorAll(".work-month-directory")
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
                    if (!system.running) {
                        const finished = document.querySelector(".status-container .finished")
                        const started = document.querySelector(".status-container .started")
                        const notStarted = document.querySelector(".status-container .not-started")
                        !started.classList.contains("d-none") && finished.classList.add("d-none")
                        !finished.classList.contains("d-none") && finished.classList.add("d-none")
                        !notStarted.classList.contains("d-none") && notStarted.classList.remove("d-none")
                    }

                    directoryContainer.querySelectorAll(".work-month-directory-selected")
                        .forEach(dir => {
                            dir.classList.contains("work-month-directory-selected")
                                && dir.classList.remove("work-month-directory-selected");
                            
                            dir.querySelector(".bi-folder").classList.remove("d-none");
                            dir.querySelector(".bi-folder2-open").classList.add("d-none");
                        });
                    
                    if (!directoryModel.classList.contains("work-month-directory-selected")){
                        directoryModel.classList.add("work-month-directory-selected");
                        directoryModel.querySelector(".bi-folder").classList.toggle("d-none");
                        directoryModel.querySelector(".bi-folder2-open").classList.toggle("d-none");
                    }

                    setData(month);
                })
            })
            
            const folders = document.querySelectorAll(".month-directories .work-month-directory");
            if (folders.length > 0) {
                folders.forEach(folder => {
                    folder.addEventListener("contextmenu", (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        contextMenuCurrentFolder.element = folder;
                        contextMenuCurrentFolder.title = folder.querySelector(".folder-title")
                            .textContent.replace("/", "-");
                            
                        showFolderContextMenu(folder);                 
                    })
                })
            }
        }
    })
    setData(actualWorkMonth);
}


const splashScreen = {
    "show": () => alertBackdrop.querySelector("strong").textContent = "Inicializando..",
    "dismiss": () => alertBackdrop.classList.remove("d-none")
}


window.onload = () => {
    isUserSet().then(response => {
        splashScreen.show();
        if(response) {
            containerContent.classList.remove("d-none");
            splashScreen.dismiss();
            setSelectMonths();
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

window.addEventListener('keyup', e => {
	if (e.key === 93){
		e.preventDefault();
		return false;
	}
})