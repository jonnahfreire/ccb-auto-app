const containerUserRequest = _$(".container-request-user-credentials");
const userCredentialInputs = _$$(".user-credential-input");

const user            = _$("#user");
const password        = _$('#pass');
const confirmPassword = _$('#pass-confirm');

const alertBackdrop     = _$(".backdrop-alert");

const containerContent         = _$(".container-content");
const containerContentHeader   = _$(".container-content-header");
const content                  = _$(".container-content .content");
const folderContextMenu        = $(".folder-context-menu").this;
const contextMenuCurrentFolder = {"element": "", "title": ""};
const timeout = 100;
const statusCheckInterval = 500;
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
        
        if (password.value || confirmPassword.value) {
            inputElement.setAttribute('type', type);
            el.classList.toggle('fa-eye-slash');
            el.classList.add('fa-eye');
        }
    });
}

// Set user
$("#form-user-credentials").on("submit", (e) => {
    e.preventDefault();
    
    const passSuccessIcons = [
        $(".user-icon-success"),
        $(".pass-icon-success"),
        $(".pass2-icon-success")
    ]
    const passEyeIcons = [
        $('#togglePassword'),
        $('#toggleConfirmPassword')
    ]

    if(user.value.length > 0 && password.value.length > 0 
        && confirmPassword.value.length > 0 
        && password.value === confirmPassword.value) {
        
        passSuccessIcons.forEach(icon => icon.removeClass("d-none"));
        passEyeIcons.forEach(icon => icon.addClass("d-none"));

        $(".pass-feedback").addClass('d-none');

        const username = user.value;
        const pass = password.value;
        
        // send to database
        setUserCredentials(username, pass).then(response => {
            
            if (response) {
                Array.prototype.slice.call(userCredentialInputs)
                    .forEach(input => input.value = "");

                $("#user-success-inserted-alert").removeClass("d-none");
                
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
                $("#user-failed-insert-alert").removeClass("d-none")
            }
        })
        
    } else {
        passSuccessIcons.slice(1).forEach(icon => icon.addClass("d-none"));
        passEyeIcons.forEach(icon => icon.removeClass("d-none"));
        $(".pass-feedback").removeClass('d-none');
    }
})


const getMappedObject = obj => {
    const map = {
        "keys": [], 
        "values": Object.values(obj)
    }
     
    Object.keys(obj).map(key => {
        
        if (key.includes("-")) {
            key = key.split("-")
            const isNumber = Number.parseInt(key[1]) ? true: false;

            key = !isNumber
            ? key[0].concat(key[1].replace(key[1][0], key[1][0].toUpperCase()))
            : key[0]+key[1];
        }
        map.keys.push(key);
    });

    const mapped = {"data": {}}

    for (let index = 0; index < map.keys.length; index++) {
        const key = map.keys[index];
        const value = map.values[index]
        
        const item = mapped.data[`${key}`] = value;
        if (!item in mapped) mapped.data = {...mapped.data, item}
    }

    return mapped.data;
}

// perfil
$(".perfil").on("click", () => {
    $(".perfil-modal-info").toggleClass("d-none");
    $(".perfil-modal-info").addClass("p-m-opacity");
})

// Remove user
$(".perfil-modal-info .remove-user").on("click", () => {
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
$(".perfil-modal-info .settings").on("click", () => {
    const content = $(".content")
    const settingsContainer = $(".container-settings")

    content.addClass("d-none");
    settingsContainer.removeClass("d-none");

    $(".container-settings .btn-go-back").on("click", () => {
            settingsContainer.addClass("d-none");
            content.removeClass("d-none");
    })
    
    document.onkeyup = function(e) {
        if (e.altKey && e.key === "ArrowLeft") {
            settingsContainer.addClass("d-none");
            content.removeClass("d-none");
        }
    };
})

// Perfil modal
$(".container-settings").on("click", () => {
    $(".perfil-modal-info").addClass("d-none");
    $(".perfil-modal-info").removeClass("p-m-opacity");
})

$(".content").on("click", () => {
    $(".perfil-modal-info").addClass("d-none");
    $(".perfil-modal-info").removeClass("p-m-opacity");
})

$("body").on("click", () => {
    $(".folder-context-menu").addClass("d-none");
    $(".folder-context-menu").removeClass("f-c-opacity");
})

$(".btn-create").on("click", () => {
    const modalSelectBackdrop = $(".select-month-modal-backdrop");
    modalSelectBackdrop.removeClass("d-none");

    let selectedMonth = null;
    $(".modal-select-month svg").on("click", () => {
        modalSelectBackdrop.addClass("d-none");
    })

    $("#work-month-select").on('change', (e) => {
        selectedMonth = e.target.value;
    })

    $(".select-month-modal-backdrop .btn-ok").on("click", () => {
        modalSelectBackdrop.addClass("d-none")   
        
        selectedMonth && createWorkDirectory(selectedMonth)
            .then(response => response && init())
    })
})

$(".btn-add").on("click", () => {
    getFilesFromFolder().then(response => response && init())
})

// Automation Start
$(".btn-start").on("click", async() => {
    const monthDirectories = _$$(".month-directories .work-month-directory");
        
    const selectedMonthDir = [...monthDirectories].filter(month => {
            if ($(month).containClass("work-month-directory-selected")){
                return month
            }
        })[0];

    const selectedMonth = $(selectedMonthDir).get(".folder-title", el => el.text());
    
    const workMonthPath = await getWorkMonthPath(selectedMonth);
    
    getData(selectedMonth.replace("/", "-")).then(response => {
        const debts1000 = response["1000"]
        const debts1010 = response["1010"]

        const allDebts = [...debts1000, ...debts1010];
        
        const items = [..._$$(".debt-info")];
        const files = {"success": [], "error": []};

        if (debts1000 || debts1010) {
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
                        if (!$(".status-container .not-started").containClass("d-none")) {
                            $(".status-container .not-started").addClass("d-none");
                            $(".status-container .started").removeClass("d-none");   
                        }
                        
                        if (!$(".not-started").containClass("d-none")) {
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

                        $(".status-container .started").addClass("d-none");
                        $(".status-container .finished").removeClass("d-none");
                        clearInterval(statusCheck);
                    }                        
                })
            }, statusCheckInterval);
        }
    })
})
// End Automation


const getMonths = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const actualMonth = month < 9 ? `0${month+1}/${year}`: `${month+1}/${year}`;

    const months = []

    for (let index = 1; index <= 12; index++) {
        months.push( index < 10 ? `0${index}/${year}`: `${index}/${year}` );
    }

    return {months, actualMonth};
}


const setSelectMonths = () => {
    const {months, actualMonth} = getMonths();

    const options = $$("#work-month-select option").this;
    if (options.length == 14) return actualMonth;

    months.map(month => {
        const option = _$("#work-month-select option").cloneNode(true);
        const select = _$("#work-month-select");
        
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

    // clear content
    account == "1000" && _$$(".account1000-content .model-item")
        .forEach(item => item.remove());
    
    account == "1010" && _$$(".account1010-content .model-item")
        .forEach(item => item.remove());
        
    if(debtList.length > 0) {
        debtList.forEach(debt => {
            const debtValue = new Intl.NumberFormat(`pt-BR`, {
                currency: `BRL`,
                style: 'currency',
            }).format(debt.value.replace(",","."));

            const model = _$(".content-model .debt-info").cloneNode(true);
            
            if (debt.fileType === "pdf") {
                $(model).get(".filetype svg.pdf", el => el.removeClass("d-none"));

            } else if (debt.fileType === "jpg" || debt.fileType === "jpeg") {
                $(model).get(".filetype svg.jpg", el => el.removeClass("d-none"));

            }else if (debt.fileType === "png") {
                $(model).get(".filetype svg.png", el => el.removeClass("d-none"));
            }

            if (debt.fileName.includes("DB AT")) {
                let fileName = debt.fileName.replace("DB AT", "");
                fileName = fileName.length > 12 ? `${fileName.slice(0, 12)}...`: fileName;
                $(model).get(".filename", el => el.setText(fileName));

            } else {
                $(model).get(".filename", el=> el.setText(debt.fileName));
            }

            const date = `${debt.date[0]}/${debt.date[1]}/${debt.date[2]}`;

            $(model).get(".filedate", el => el.setText(date));
            $(model).get(".filevalue", el => el.setText(debtValue));
            $(model).get(".filedebttype", el => el.setText("DP " + debt.expenditure));
               
            account === "1000" && $(".account1000-content .message").addClass("d-none");
            account === "1010" && $(".account1010-content .message").addClass("d-none");
            
            account === "1000" && _$(".account1000-content").append(model);
            account === "1010" && _$(".account1010-content").append(model);
        })
    } else {
        account === "1000" && $(".account1000-content .message").removeClass("d-none");
        account === "1010" && $(".account1010-content .message").removeClass("d-none");
    }
}


const setData = (month) => {
    getData(month)
        .then(response => {
            const debts1000 = response["1000"].map(debt => getMappedObject(debt));
            const debts1010 = response["1010"].map(debt => getMappedObject(debt));

            if (debts1000.length > 0 || debts1010.length > 0) {
                $(".status-container").removeClass("d-none");
            } else {
                $(".status-container").addClass("d-none");
            }

            fillContent(debts1000, "1000");
            fillContent(debts1010, "1010");
    })
}

folderContextMenu.querySelector(".remove-folder").addEventListener("click", () => {
    $(".remove-month-modal-backdrop").removeClass("d-none");

    // btn close (x)
    $(".modal-remove-header svg").on("click", () => {
        $(".remove-month-modal-backdrop").addClass("d-none");
    })

    //btn cancel
    $(".modal-remove-footer .btn-cancel").on("click", () => {
        $(".remove-month-modal-backdrop").addClass("d-none");
    })

    $(".modal-remove-footer .btn-ok").on("click", () => {
        $(".remove-month-modal-backdrop").addClass("d-none");

        removeMonthDirectory(contextMenuCurrentFolder.title)
            .then(response => {
                response && init();
            })
    })
})

$(folderContextMenu).get(".open-folder", folder => 
    folder.on("click", () => {
        getSysPath().then(path => {
            const folderPath = path+"/"+contextMenuCurrentFolder.title
            path && openDirectory(folderPath).then();
        })
    }
))

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

    $(".container-content .actual-month span")
        .setText(actualWorkMonth.replace("-", "/"));
    
    getUserName().then(response => {
        username = response; 
        $(".perfil .user-content #username").setText(username)
    })

    createWorkDirectory(actualWorkMonth)
        .then(response => {
            if (response === null) {
                const text = "Verificando diretório de trabalho, aguarde...";
                $(alertBackdrop).get("strong", el => el.setText(text));

            }else {
                const text = "Criando diretório de trabalho, aguarde...";
                $(alertBackdrop).get("strong", el => el.setText(text));
            }
            
            setTimeout(() => {
                $(alertBackdrop).addClass("d-none")
                $(containerContentHeader).removeClass("d-none")
                $(content).removeClass("d-none")
            }, timeout); // 2000
            
            const text = "Verificando diretório de trabalho, aguarde...";
            $(alertBackdrop).get("strong", el => el.setText(text));
        })
    
    getMonthDirectoryList().then(response => {
        if (response.length > 0) {
            const directoryContainer = _$(".month-directories");

            directoryContainer.querySelectorAll(".work-month-directory")
                .forEach(item => item.remove());
            
            response.forEach(month => {
                const directoryModel = _$(".content-model .work-month-directory").cloneNode(true);

                $(directoryModel).get(".folder-title", el => el.setText(month.replace("-", "/")));
                directoryContainer.append(directoryModel);

                if (month === actualWorkMonth) {
                    $(directoryModel).addClass("work-month-directory-selected");
                    $(directoryModel).get(".bi-folder", el => el.addClass("d-none"));
                    $(directoryModel).get(".bi-folder2-open", el => el.removeClass("d-none"));
                }

                directoryModel.addEventListener("click", () => {
                    if (!system.running) {
                        const finished = _$(".status-container .finished")
                        const started = _$(".status-container .started")
                        const notStarted = _$(".status-container .not-started")
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
                        $(directoryModel).get(".bi-folder", el => el.toggleClass("d-none"));
                        $(directoryModel).get(".bi-folder2-open", el => el.toggleClass("d-none"));
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