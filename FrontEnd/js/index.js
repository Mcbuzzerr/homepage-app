const openWindow = async (event, windowType) => {
    const window = await getWindow(windowType);
    // const windowFrame = document.createElement('div');
    console.log(window);
    document.body.appendChild(window);
    let rect = event.target.getBoundingClientRect();
    if (rect.left + window.clientWidth > document.body.clientWidth) {
        window.style.left = document.body.clientWidth - window.clientWidth - 60 + 'px';
    } else {
        window.style.left = rect.left + 50 + 'px';
    }
    if (rect.top + window.clientHeight > document.body.clientHeight) {
        window.style.top = document.body.clientHeight - window.clientHeight - 60 + 'px';
    } else {
        window.style.top = rect.top + 50 + 'px';
    }
}

const getWindow = async (windowType) => {
    let window;
    switch (windowType) {
        case "profiles":
            let html = `<div class="profile-list">`

            let results = await fetch("http://localhost:8001/profiles")
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.length; i++) {
                        html += `<div class="profile-list-item" id="${data[i]._id}">
                                    <div class="profile-icon icon-${data[i].icon}"></div>
                                    <div class="profile-name"><span>${data[i].name}</span></div>
                                    <div class="button profile-select"><span>Select</span></div> 
                                    <div class="button profile-edit"><span>Edit</span></div> 
                                </div>`
                    }
                    html += `</div>`
                })
                

            return window = createWindow(html, "Profiles", 400, 500);
        case "watchlists":
            return window = createWindow("Hello World", "WatchLists", 300, 300);
        default:
            alert("Error: Window type not found");
            return window = createWindow("Window Not Found", "Error", 300, 300);
        }
}


const createWindow = (content, title, width, height) => {
    let window = document.createElement('div');
    window.classList.add('window');
    window.style.setProperty('--window-width', width + 'px');
    window.style.setProperty('--window-height', height + 'px');
    // TODO: Create Profiles window
    // TODO: Create WatchList window
    window.innerHTML = `<div class="window-header">
                            <div class="window-header-title">
                                ${title}
                            </div>
                            <div class="window-header-button window-header-close-button" onclick="closeWindow(event)">
                                
                            </div>
                        </div>
                        <div class="window-content">
                            ${content}
                        </div>`;
    window.firstChild.firstElementChild.addEventListener('mousedown', (event) => {
        let rect = window.getBoundingClientRect();
        let offsetX = event.clientX - rect.left;
        let offsetY = event.clientY - rect.top;
        window.style.position = 'absolute';
        window.style.zIndex = 1000;
        document.body.append(window);
        moveAt(event.pageX, event.pageY);
        function moveAt(pageX, pageY) {
            window.style.left = pageX - offsetX + 'px';
            window.style.top = pageY - offsetY + 'px';
        }
        function onMouseMove(event) {
            moveAt(event.pageX, event.pageY);
        }
        document.addEventListener('mousemove', onMouseMove);
        window.onmouseup = function() {
            document.removeEventListener('mousemove', onMouseMove);
            window.onmouseup = null;
        };
    });
    window.firstChild.ondragstart = function() {
        return false;
    };
    return window;
}

const closeWindow = (event) => {
    event.target.parentElement.parentElement.remove();
}

const checkPlaceHolder = (event) => {
    let placeHolder = document.getElementById("placeHolderText");
    if (event.target.value == "") {
        placeHolder.style.display = "block";
    } else {
        placeHolder.style.display = "none";
    }
}