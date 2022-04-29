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
const timeout = 1000;
const statusCheckInterval = 100;
const automation = {"running": false};


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

async function clearStatus() {
    return await eel.clear_status()()
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

async function createWorkingDirectory(month) {
    return await eel.create_work_directory(month)()
};

async function insertItem(month, workMonthPath, itemsList, window=false) {
    return await eel.insert_new_item(month,workMonthPath, itemsList, window)()
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

async function removeNotification(id) {
    return await eel.remove_notification(id)()
};

async function removeAllNotifications() {
    return await eel.clear_all_notifications()()
};

async function getNotifications() {
    return await eel.get_notification_list()()
};

async function monthHasInsertedDebts(month) {
    return await eel.month_has_inserted_debts(month)()
}

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


const handleFormCredentialSubmit = (e) => {
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
}


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


const handleRemoveUser = () => {
    const removeUserBackdrop = _$(".remove-user-modal-backdrop");
    $(removeUserBackdrop).removeClass("d-none");
    
    const removeUserModal = $(".modal-remove-user");
    
    const btnCancel = [
        _$(removeUserModal).get("svg"),
        _$(removeUserModal).get(".btn-cancel")
    ]
    
    btnCancel.forEach(btn => 
        $(btn).on("click", () => $(removeUserBackdrop).addClass("d-none")))
        
        const btnOk = _$(removeUserModal).get(".modal-remove-user-footer .btn-ok");
        $(btnOk).on("click", () => {
            removeCurrentUser().then(response => {
                response && window.location.reload();
            })
        });
};
    
const handleSettingsClick = () => {
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
};


const handleContainerSettingsClick = () => {
    !_$(".notification-items-container").classList.contains("d-none")
    && $(".notification-items-container").addClass("d-none");

    $(".perfil-modal-info").addClass("d-none");
};

const handleOpenPerfil = () => {
    !_$(".notification-items-container").classList.contains("d-none")
    && $(".notification-items-container").addClass("d-none");

    $(".perfil-modal-info").toggleClass("d-none");
}

const handleContentClick = () => {
    $(".perfil-modal-info").addClass("d-none");
};

const handleBodyClick = () => {
    $(".popover-finished-debts").addClass("d-none");
    $(".folder-context-menu").addClass("d-none");
    
    $(".folder-context-menu").removeClass("f-c-opacity");
};

const handleCreateWorkingMonth = () => {
    if (automation.running) {
        modalAlertSysRunning.show("Não é possível criar diretórios enquanto existir lançamentos em andamento.");
        return false;
    }
    
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
        
        selectedMonth && createWorkingDirectory(selectedMonth)
            .then(response => response && init())
    })
};

const handleAddItems = () => {
    if (automation.running) {
        modalAlertSysRunning.show("Não é possível inserir despesas ou receitas enquanto existe lançamentos em andamento.");
        return false;
    }
    getFilesFromFolder().then(response => response && init())
};

const notifications = {
    items: [],
    animate: () => {
        _$(".notifications .bell").style.animationDuration = ".2s";
        _$(".notifications .notify-sign").style.animationDuration = ".2s";
    },
    stop: () => {
        _$(".notifications .bell").style.animationDuration = "0s";
        _$(".notifications .notify-sign").style.animationDuration = "0s";
    },
    hide: () => {
        notifications.items.length == 0 
        && (_$(".notifications .notify-sign").style.display = "none")
        && $(".notifications .no-notifications").removeClass("d-none");

        !_$(".notifications .notification-items-container").classList.contains("d-none")
        && $(".notifications .notification-items-container").addClass("d-none");
    },
    show: () => {
        !_$(".perfil-modal-info").classList.contains("d-none")
        && $(".perfil-modal-info").addClass("d-none");

        if (notifications.items.length > 0){
            $(".notifications .clear-notifications").removeClass("d-none");
            $(".notifications .notification-clear-all span").on("click", () => {
                notifications.removeAll();
            });
        }

        $(".notifications .notification-items-container").removeClass("d-none");

        $(".content").on("click", () => notifications.hide());
    },
    isHidden: () => {
        return _$(".notifications .notification-items-container").classList.contains("d-none")
    },
    isShown: () => {
        return !_$(".notifications .notification-items-container").classList.contains("d-none")
    },
    toggle: () => {
        if (notifications.isShown()) notifications.hide();
        else notifications.show();
    },
    update: () => notifications.getNotifications(),
    intervals: [],
    getNotifications: () => {
        getNotifications().then(response => {
            notifications.items = response;

            notifications.setNotifications(notifications.items);

            let animInterval = null;
            if (notifications.items.length > 0){
                $(".notifications .no-notifications").addClass("d-none");
                _$(".notifications .notify-sign").style.display = "flex";
                
                animInterval = setInterval(()=> {
                    notifications.animate();
                
                    setTimeout(()=> notifications.stop(), 2000);
                }, 10000);
                notifications.intervals.push(animInterval);
    
            } else {
                $(".notifications .clear-notifications").addClass("d-none");
                $(".notifications .no-notifications").removeClass("d-none");
                _$(".notifications .notify-sign").style.display = "none";
                notifications.stop();
                notifications.intervals
                    .forEach(interval => clearInterval(interval))
            }
        })    
    },
    setNotifications: (notificationData) => {
        _$$(".notification-item-container .notification-item")
            .forEach(item => item.remove());

        notificationData.forEach(item => {
            const notificationItem = _$(".content-model .notification-item").cloneNode(true);
            
            notificationItem.setAttribute("data-id", item.id)

            notificationItem.querySelector(".notification-details-header")
                .textContent = item.header;
            
            item.icon === "danger"
            && notificationItem.querySelector(".notification-item-icon .text-danger")
                .classList.remove("d-none");
            
            item.icon === "success"
            && notificationItem.querySelector(".notification-item-icon .text-success")
                .classList.remove("d-none");

            notificationItem.querySelector(".title")
                .textContent = item.title;

            notificationItem.querySelector(".message")
                .textContent = item.message;
            
            _$(".notifications .notification-item-container")
                .append(notificationItem);

            notificationItem.querySelector(".notification-delete-x")
                .addEventListener("click", () => {
                    removeNotification(item.id)
                        .then(response => {
                            if (response) {
                                notificationItem.style.animationPlayState = "running";
                                setTimeout(() => notifications.removeItem(notificationItem), 1000);
                            }
                        })
                })
        })
    },
    removeItem: (item) => {
        item.remove();
        notifications.getNotifications();
    },
    removeAll: () => {
        _$$(".notifications .notification-item")
            .forEach(item => {
                id = Number.parseInt(item.getAttribute("data-id"));
                item.style.animationPlayState = "running";
                
                removeNotification(id)
                    .then(response => {
                        if (response) {
                            setTimeout(() => notifications.removeItem(item), 1000);
                        }
                    })
            });
        setTimeout(() => notifications.getNotifications(), 1000);
    }
}


const updateStatus = (items, status, interval) => {
    notifications.update();

    if (Object.keys(status.current).length === 0) return false;
                    
    const currentFileName = status.current["file-name"]
    const current = items.filter(item => 
        currentFileName.includes(item.querySelector(".file-name").textContent.trim())
    )[0]

    if (status.started && !status.finished_all){
        if (!$(".status-container .starting").containClass("d-none")) {
            $(".status-container .starting").addClass("d-none");
            $(".status-container .started").removeClass("d-none");
        }
        
        if (!current.querySelector(".not-started").classList.contains("d-none")) {
            current.querySelector(".not-started").classList.add("d-none");
            current.querySelector(".started").classList.remove("d-none");    
        }
        
        if (current.querySelector(".started").classList.contains("d-none")) {
            current.querySelector(".started").classList.remove("d-none"); 
        }

        if (status.finished) {                           
            current.querySelector(".started").classList.add("d-none"); 
            current.querySelector(".finished").classList.remove("d-none");
        }

        if (status.failed) {
            current.querySelector(".not-started").classList.add("d-none");
            current.querySelector(".started").classList.add("d-none"); 
            current.querySelector(".finished").classList.add("d-none"); 
            current.querySelector(".failed").classList.remove("d-none");
            
            current.querySelector(".status-error-msg .error-message")
                .textContent = status.fail_cause

            current.querySelector(".failed").addEventListener("mouseover", () => {
                current.querySelector(".status-error-msg").classList.remove("d-none")
            })

            current.querySelector(".failed").addEventListener("mouseout", () => {
                current.querySelector(".status-error-msg").classList.add("d-none")
            })
        }
    }
    
    if (status.finished_all) {
        if (!status.failed) {
            current.querySelector(".started").classList.add("d-none"); 
            current.querySelector(".finished").classList.remove("d-none");
        } else {
            current.querySelector(".finished").classList.add("d-none");
            current.querySelector(".started").classList.add("d-none"); 
            current.querySelector(".failed").classList.remove("d-none");
        }
        
        $(".status-container .started").addClass("d-none");
        $(".status-container .finished").addClass("d-none");

        if (status.finished_all_with_exceptions) {
            $(".status-container .finished-with-exceptions").removeClass("d-none");

        } else if(status.failed_all) {
            $(".status-container .finished-with-fail").removeClass("d-none");

        } else {
            $(".status-container .finished").removeClass("d-none");
        }

        clearInterval(interval);
        clearStatus();
        automation.running = false;
    }
};

const startInsertions = async() => {
    if (automation.running) {
        modalAlertSysRunning.show("Já existe um processo em andamento, aguarde finalizar.");
        return false;
    }
    
    const monthDirectories = _$$(".month-directories .work-month-directory");
    if (monthDirectories.length == 0) {
        return false;
    }
    
    const selectedMonthDir = [...monthDirectories].filter(month => {
            if ($(month).containClass("work-month-directory-selected")){
                return month
            }
        })[0];
    
    const selectedMonth = $(selectedMonthDir).get(".folder-title", el => el.text());
    const workMonthPath = await getWorkMonthPath(selectedMonth);
    
    getData(selectedMonth.replace("/", "-")).then(response => {
        const items1000 = response["1000"]
        const items1010 = response["1010"]
    
        const allItems = [...items1000, ...items1010];
        const items = $$(".debt-info");
        const files = {"success": [], "error": []};
    
        if (allItems.length > 0) {
            insertItem(selectedMonth, workMonthPath, allItems, true);
    
            automation.running = true;
    
            $(".status-container .not-started").addClass("d-none");
            $(".status-container .starting").removeClass("d-none");        
    
            const statusCheck = setInterval(() => {
                getStatus().then(response => {
                    const status = response.status;
                    const errors = response.errors;
                    
                    updateStatus(items, status, statusCheck);                      
                })
            }, statusCheckInterval);
        } else {
            modalAlertItemsNotFound.show();
        }
    })
};


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


const fillContent = (itemList, account) => {

    if (automation.running) {
        return false;
    }

    // clear content
    account == "1000" && _$$(".account1000-content .model-item")
        .forEach(item => item.remove());
    
    account == "1010" && _$$(".account1010-content .model-item")
        .forEach(item => item.remove());
        
    if(itemList.length > 0) {
        itemList.forEach(item => {
            const itemValue = new Intl.NumberFormat(`pt-BR`, {
                currency: `BRL`,
                style: 'currency',
            }).format(item.value.replace(",","."));

            const model = _$(".content-model .debt-info").cloneNode(true);
            
            if (item.fileType === "pdf") {
                $(model).get(".file-type svg.pdf", el => el.removeClass("d-none"));

            } else if (item.fileType === "jpg" || item.fileType === "jpeg") {
                $(model).get(".file-type svg.jpg", el => el.removeClass("d-none"));

            }else if (item.fileType === "png") {
                $(model).get(".file-type svg.png", el => el.removeClass("d-none"));
            }

            if (item.fileName.includes("DB AT")) {
                let fileName = item.fileName.replace("DB AT", "");
                fileName = fileName.length > 12 ? `${fileName.slice(0, 12)}...`: fileName;
                $(model).get(".file-name", el => el.setText(fileName));

            } else {
                $(model).get(".file-name", el=> el.setText(item.fileName));
            }

            const date = `${item.date[0]}/${item.date[1]}/${item.date[2]}`;

            $(model).get(".file-date", el => el.setText(date));
            $(model).get(".file-value", el => el.setText(itemValue));

            if (item.insertType === "MOVINT") {
                $(model).get(".file-insert-type", el => el.setText(`${item.type} ${item.destAccount}`));

            } else {
                $(model).get(".file-insert-type", el => el.setText("DP " + item.expenditure));
            }
               
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
            const items1000 = response["1000"].map(item => getMappedObject(item));
            const items1010 = response["1010"].map(item => getMappedObject(item));

            if (items1000.length > 0 || items1010.length > 0) {
                $(".status-container").removeClass("d-none");
            } else {
                $(".status-container").addClass("d-none");
            }

            fillContent(items1000, "1000");
            fillContent(items1010, "1010");
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

const showMonthPopover = (element) => {
    const windowRightCorner = window.innerWidth;
    const position = getPosition(element)
    
    const elementRight = element.getBoundingClientRect().right;
    const elementLeft = element.getBoundingClientRect().left;
    
    const monthPopover = _$(".popover-finished-debts");
    $(".popover-finished-debts").removeClass("d-none");

    $$(".month-directories .work-month-directory").on("mouseout", () => {
        $(".popover-finished-debts").addClass("d-none")
    })

    if (elementRight >= windowRightCorner){
        monthPopover.style.left = 
            windowRightCorner - monthPopover
            .getBoundingClientRect()
            .width - 20 + "px";

    } else if (elementLeft <= 0){
        monthPopover.style.left = 20 + "px";

    } else {
        monthPopover.style.left = elementLeft + "px";
    }
    monthPopover.style.top = position.y + 60 + "px";
}


const handleFolderClick = (directoryContainer, directoryModel, month) => {
    if (!automation.running) {  
        const notStarted = _$(".status-container .not-started");
        !$(notStarted).containClass("d-none") && $(notStarted).removeClass("d-none");
        
        const statusItems = [
            _$(".status-container .started"),
            _$(".status-container .finished"),
            _$(".status-container .finished-with-fail"),
            _$(".status-container .finished-with-exceptions")
        ]

        statusItems.forEach(item => {
            !(item.classList.contains("d-none"))
            && _$(item).classList.add("d-none");
        })
        
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

    } else {
        modalAlertSysRunning.show("Não é possível visualizar os mêses enquanto a automação está em andamento.");
    }
};

const setDirectories = (directoriesData, currentMonth) => {
    if (directoriesData.length > 0) {
        const directoryContainer = _$(".month-directories");

        directoryContainer.querySelectorAll(".work-month-directory")
            .forEach(item => item.remove());
        
        directoriesData.forEach(month => {
            const directoryModel = _$(".content-model .work-month-directory").cloneNode(true);

            $(directoryModel).get(".folder-title", el => el.setText(month.replace("-", "/")));
            directoryContainer.append(directoryModel);

            if (month === currentMonth) {
                $(directoryModel).addClass("work-month-directory-selected");
                $(directoryModel).get(".bi-folder", el => el.addClass("d-none"));
                $(directoryModel).get(".bi-folder2-open", el => el.removeClass("d-none"));
            }

            $(directoryModel).on("click", () => {
                handleFolderClick(directoryContainer, directoryModel, month);   
            })
        })

        handleMonthPopover();
        handleFolderContextClick();
    }
};

const modalAlertSysRunning = {
    backdrop: null,
    show: (msg) => {
        const backdrop = _$(".system-running-modal-backdrop")
        backdrop.classList.remove("d-none");
        modalAlertSysRunning.backdrop = backdrop;

        backdrop.querySelector(".modal-alert-running .alert-message")
            .textContent = msg;

        const btnClose = [
            backdrop.querySelector(".btn-ok"),
            backdrop.querySelector("svg")                            
        ]
    
        btnClose.forEach(btn => {
            btn.addEventListener("click", () => {
                backdrop.classList.add("d-none");
            });
        });
    },
    hide: () => modalAlertSysRunning.backdrop.classList.add("d-none")
};

const modalAlertItemsNotFound = {
    backdrop: null,
    show: () => {
        const backdrop = _$(".system-running-modal-backdrop")
        backdrop.classList.remove("d-none");
        modalAlertItemsNotFound.backdrop = backdrop;
        
        backdrop.querySelector(".modal-alert-running .modal-alert-title")
            .textContent = "Atenção!";

        backdrop.querySelector(".modal-alert-running .alert-message")
            .textContent = "Não foi encontrado lançamentos a ser realizado para o mês selecionado. Insira lançamentos.";

        const btnClose = [
            backdrop.querySelector(".btn-ok"),
            backdrop.querySelector("svg")                            
        ]
    
        btnClose.forEach(btn => {
            btn.addEventListener("click", () => {
                backdrop.classList.add("d-none");
            });
        });
    },
    hide: () => modalAlertItemsNotFound.backdrop.classList.add("d-none")
};

const init = () => {
    const currentWorkingMonth = setSelectMonths().replace("/", "-");

    $(".container-content .current-month span")
        .setText(currentWorkingMonth.replace("-", "/"));
    
    getUserName().then(username => {
        username && $(".perfil .user-content #username").setText(username)
    })

    createWorkingDirectory(currentWorkingMonth)
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
        response && setDirectories(response, currentWorkingMonth);
    })
    setData(currentWorkingMonth);
}

const handleMonthPopover = () => {
    $$(".month-directories .work-month-directory").on("mouseenter", (e) => {
        const month = e.target.textContent.trim().replace("/", "-");
        
        folderContextMenu.classList.contains("d-none") &&
        monthHasInsertedDebts(month).then(response => {
            response && showMonthPopover(e.target);
        })
    })
}

const handleFolderContextClick = () => {
    const folders = _$$(".month-directories .work-month-directory");

    if (folders.length > 0) {
        folders.forEach(folder => {
            folder.addEventListener("contextmenu", (e) => {
                e.preventDefault();
                e.stopPropagation();

                $(".popover-finished-debts").addClass("d-none");
                
                contextMenuCurrentFolder.element = folder;
                contextMenuCurrentFolder.title = folder.querySelector(".folder-title")
                    .textContent.replace("/", "-");
                    
                showFolderContextMenu(folder);                 
            })
        })
    }
}

const splashScreen = {
    "show": () => alertBackdrop.querySelector("strong").textContent = "Inicializando..",
    "dismiss": () => alertBackdrop.classList.remove("d-none")
}

const listeners = {
    start: () => {
        // Set user
        $("#form-user-credentials").on("submit", (e) => handleFormCredentialSubmit(e));

        // Notifications
        $(".notifications .bell").on("click", () => notifications.toggle());

        // Automation Start
        $(".btn-start").on("click", startInsertions);

        // Add Items
        $(".btn-add").on("click", handleAddItems);

        // Create working month directory
        $(".btn-create").on("click", handleCreateWorkingMonth);

        // Perfil click
        $(".container-settings").on("click", handleContainerSettingsClick);
        
        // Content click
        $(".content").on("click", handleContentClick);
        
        // Body click
        $("body").on("click", handleBodyClick);
        
        // Open perfil modal
        $(".perfil").on("click", handleOpenPerfil);
        
        // Remove user
        $(".perfil-modal-info .remove-user").on("click", handleRemoveUser);

        // Settings
        $(".perfil-modal-info .settings").on("click", handleSettingsClick);
    }
};

window.onload = () => {
    listeners.start();

    isUserSet().then(response => {
        splashScreen.show();
        if(response) {
            containerContent.classList.remove("d-none");
            splashScreen.dismiss();
            setSelectMonths();
            setTimeout(() => init(), timeout); //1000

            notifications.getNotifications();
        }

        toggleInputPass(togglePassword, password);
        toggleInputPass(toggleConfirmPassword, confirmPassword);
        !response && containerUserRequest.classList.remove("d-none");
    })
}


// $(window).on('contextmenu', e => {
//     if (e.button == 2){
//         e.preventDefault();
//         return false;
//     }
// })

$(window).on('keyup', e => {
    if (e.key === 93){
        e.preventDefault();
        return false;
    }
})