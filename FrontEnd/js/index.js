let currentPageID = 1;
let columnCount = 8;
let rowCount = 4;
let itemCount = 32;

let userGrid = [];
for (let i = 0; i < itemCount * 2; i++) {
    userGrid[i] = null;
}
// Randomly add cats to grid
for (let i = 0; i < itemCount / 2; i++) {
    let index = Math.floor(Math.random() * itemCount * 2);
    userGrid[index] = i;
}


window.onload = () => {
    setIconHidden(0, true);
    generateGrid(1, columnCount, rowCount, itemCount);
    // let profile = JSON.parse(localStorage.getItem("profile"));
    // if (profile == null) {
    //     document.getElementById("profileName").innerHTML = "No Profile Selected";
    // } else {
    //     document.getElementById("profileName").innerHTML = profile.name;
    // }
}

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
    let html;
    let results;
    switch (windowType) {
        case "profiles":
            html = `<div class="resource-list">`

            // results = await fetch("http://localhost:80/profile/all")
            //     .then(response => response.json())
            //     .then(data => {
            //         for (let i = 0; i < data.length; i++) {
            //             html += `<div class="resource-list-item" id="${data[i]._id}">
            //                         <div class="resource-icon icon-${data[i].icon}"></div>
            //                         <div class="resource-name"><span>${data[i].name}</span></div>
            //                         <div class="button resource-select" onclick="selectProfileClickHandler(event)"><span>Select</span></div> 
            //                         <div class="button resource-edit" onclick="editProfileClickHandler(event)"><span>Edit</span></div> 
            //                     </div>`
            //         }
            //         html += `</div>`
            //     })
                

            return window = createWindow(html, "Profiles", 400, 500);
        case "watchlists":
            html = `<div class="resource-list">`
            let userID = JSON.parse(localStorage.getItem("profile"))._id;
            userID = userID.split("/")[userID.split("/").length - 1]
            // results = await fetch("http://localhost:80/watchList/fromProfile/" + userID)
            //     .then(response => response.json())
            //     .then(data => {
            //         for (let i = 0; i < data.length; i++) {
            //             html += `<div class="resource-list-item" id="${data[i]._id}">
            //                         <div class="resource-name"><span>${data[i].title}</span></div>
            //                         <div class="button resource-select" onclick="selectWatchListClickHandler(event)"><span>Select</span></div>
            //                         <div class="button resource-edit" onclick="editWatchListClickHandler(event)"><span>Edit</span></div>
            //                     </div>`
            //         }
            //         html += `</div>`
            //     })
            return window = createWindow(html, "WatchLists", 300, 300);
        case "add-service":
            return window = createWindow("Add Service Window", "Add Service", 300, 300);
        case "add-folder":
            return window = createWindow("Add Folder Window", "Add Folder", 300, 300);
        case "dev":
            return window = createWindow("Dev Window", "Dev", 300, 300);
        default:
            return window = createWindow("Window Not Found", "Error", 300, 300);
        }
}

const selectProfileClickHandler = (event) => {
    let profileID = event.target.parentElement.parentElement.id;
    let profile = fetch(`http://localhost:80/profile/${profileID}`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem("profile", JSON.stringify(data));
        })
}

const editProfileClickHandler = (event) => {
    // TODO: Create edit profile window
}

const selectWatchListClickHandler = (event) => {
    // TODO: Create select watchlist window
}

const editWatchListClickHandler = (event) => {
    // TODO: Create edit watchlist window
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
        window.style.zIndex = 2;
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

const generateGrid = (gridID, columnCount, rowCount, itemCount) => {
    let gridPage = document.getElementById(`gp-${gridID}`);
    gridPage.style.setProperty('--column-count', columnCount);
    gridPage.style.setProperty('--row-count', rowCount);
    for (let i = ((gridID - 1) * itemCount); i < ((gridID - 1) * itemCount) + itemCount; i++) {
        let gridCell = document.createElement('div');
        gridCell.classList.add('gridCell');
        gridCell.id = "gc-" + i;

        let gridCellContent = document.createElement('div');
        gridCellContent.classList.add('gridItem');
        gridCellContent.id = "gi-" + i;

        let slotIDLabel = document.createElement('span');
        slotIDLabel.classList.add('slotID');
        slotIDLabel.innerHTML = i;
        
        gridCellContent.append(slotIDLabel);

        let sampleImage = document.createElement('div');
        sampleImage.style.backgroundImage = "url(https://cataas.com/cat?width=100&height=100)";
        sampleImage.classList.add('gridImage');
        sampleImage.id = "im-" + i;

        gridCellContent.append(sampleImage);

        let sampleText = document.createElement('span');
        sampleText.classList.add('gridText');
        sampleText.innerHTML = userGrid[i];
        if (userGrid[i] == undefined) {
            userGrid[i] = null;
            sampleText.innerHTML = "Empty";
            sampleText.style.color = "var(--lining-color)";
            sampleImage.style.backgroundImage = "none";
        }

        gridCellContent.append(sampleText);

        gridCell.append(gridCellContent);

        gridPage.append(gridCell);
    }
}

const resetGrid = (gridID) => {
    let gridPage = document.getElementById(`gp-${gridID}`);
    gridPage.innerHTML = "";
}

const toggleSize = () => {
    resetGrid(currentPageID);
    const gridBox = document.getElementById("gp-1");
    if (columnCount == 8) {
        columnCount = 4;
        itemCount = 8;
        rowCount = 2;
    } else {
        columnCount = 8;
        itemCount = 32;
        rowCount = 4;
    }
    generateGrid(currentPageID, columnCount, rowCount, itemCount);
}

const toggleIDs = () => {
    if (document.documentElement.style.getPropertyValue('--id-visibility') == "block") {
        document.documentElement.style.setProperty('--id-visibility', 'none');
    } else {
        document.documentElement.style.setProperty('--id-visibility', 'block');
    }
}

const pageSwap = (stepDirection) => {
    let nextPageID = currentPageID + stepDirection;
    let gridPages = document.getElementsByClassName("gridPage");
    if ((nextPageID) == gridPages.length) {
        newPage();
        setIconHidden(0, false);
    } else if (nextPageID == 1) {
        setIconHidden(0, true);
    } else {
        setIconHidden(0, false);
    }
    const currentPage = gridPages[currentPageID - 1];
    const nextPage = gridPages[nextPageID - 1];
    if (currentPageID < nextPageID) {
        // alert("Page Out Left")
        currentPage.style.animation = "page-out-left 0.8s ease-in-out forwards";
        nextPage.style.animation = "page-in-right 0.8s ease-in-out forwards";
    } else {
        // alert("Page Out Right")
        currentPage.style.animation = "page-out-right 0.8s ease-in-out forwards";
        nextPage.style.animation = "page-in-left 0.8s ease-in-out forwards";
    }
    currentPageID = nextPageID;
    resetGrid(currentPageID)
    generateGrid(nextPageID, columnCount, rowCount, itemCount);
}

const newPage = () => {
    let gridpage = document.createElement('div');
    gridpage.classList.add('gridPage');
    gridpage.id = `gp-${currentPageID + 2}`;
    gridpage.style.setProperty('--column-count', columnCount);
    document.getElementById("gridContainer").append(gridpage);
    setIconPlus(1, false);
}

// const toggleIconPlus = (buttonIndex) => {
//     let pageButtons = document.getElementsByClassName("pageButton");
//     let pageButton = pageButtons[buttonIndex];

//     if (pageButton.firstElementChild.style.display == "none") {
//         pageButton.firstElementChild.style.display = "flex";
//         pageButton.lastElementChild.style.display = "none";
//     } else {
//         pageButton.firstElementChild.style.display = "none";
//         pageButton.lastElementChild.style.display = "flex";
//     }
// }

const setIconPlus = (buttonIndex, isPlus) => {
    let pageButtons = document.getElementsByClassName("pageButton");
    let pageButton = pageButtons[buttonIndex];

    if (isPlus) {
        pageButton.firstElementChild.style.display = "none";
        pageButton.lastElementChild.style.display = "flex";
    } else {
        pageButton.firstElementChild.style.display = "flex";
        pageButton.lastElementChild.style.display = "none";
    }
}

const toggleIconHidden = (buttonIndex) => {
    let pageButtons = document.getElementsByClassName("pageButton");
    let pageButton = pageButtons[buttonIndex];

    if (pageButton.firstElementChild.style.display == "none") {
        pageButton.firstElementChild.style.display = "block";
    } else {
        pageButton.firstElementChild.style.display = "none";
    }
}

const setIconHidden = (buttonIndex, isHidden) => {
    let pageButtons = document.getElementsByClassName("pageButton");
    let pageButton = pageButtons[buttonIndex];

    if (isHidden) {
        pageButton.firstElementChild.style.display = "none";
    } else {
        pageButton.firstElementChild.style.display = "block";
    }
}

let isExpanded = false;
const slide = (event) => {
    if (isExpanded) {
        event.target.parentNode.style.animation = "slideOut 0.3s ease-in-out forwards";
        isExpanded = false;
    } else {
        event.target.parentNode.style.animation = "slideIn 0.3s ease-in-out forwards";
        isExpanded = true;
        document.body.addEventListener('click', (event) => {
            if (event.target.id != "menu-Bubble") {
                document.getElementById("bc-1").style.animation = "slideOut 0.3s ease-in-out forwards";
                isExpanded = false;
            }
        })
    }
}

let draggedElement = null;
document.addEventListener("dragstart", (event) => {
    draggedElement = event.target;
    event.dataTransfer.setData("text/plain", event.target.id);
    console.log("dragstart")
    console.log(event.target.id)
});

document.addEventListener("dragover", function(event) {
    // Prevent default behavior to allow drop
    event.preventDefault();

    // Check if the target element has the 'drop-target' class
    var validDropTarget = event.target.classList.contains("gridItem") || event.target.classList.contains("gridImage");

    // If the target element is a valid drop target, change its border to indicate that it can accept the dragged element
    if (validDropTarget) {
        event.target.style.border = "2px dashed black";
    }
});

document.addEventListener("dragleave", function(event) {
    // If the target element is a valid drop target, reset its border
    if (event.target.classList.contains("gridItem") || event.target.classList.contains("gridImage")) {
        event.target.style.border = "";
    }
});


document.addEventListener("drop", function(event) {
    // Prevent default behavior to allow drop
    event.preventDefault();
    // Get the ID of the dragged element from the data transfer object
    var data = event.dataTransfer.getData("text/plain");
    var validDropTarget = event.target.classList.contains("gridItem") || event.target.classList.contains("gridImage");

    // If the target element is a valid drop target, change its border to indicate that it can accept the dragged element
    if (validDropTarget) {
        
        // Append a new element to the drop target
        let dropTarget = event.target;
        let dropSlot = dropTarget.id.substring(3, dropTarget.id.length)
        let dropTargetIdentifier = dropTarget.id.substring(0, 2)
        let gridCell;
        if (dropTargetIdentifier == "gi") {
            gridCell = dropTarget.parentNode;
        } else if (dropTargetIdentifier == "im") {
            gridCell = dropTarget.parentNode.parentNode;
        }

        let gridItem = gridCell.firstElementChild;
        console.log(gridItem)

        for (let i = 0; i < gridItem.children.length; i++) {
            if (gridItem.children[i].classList.contains("gridText")) {
                gridItem.children[i].innerHTML = data;
            }
        }
        // Change the opacity of the dragged element back to 1
        draggedElement.style.opacity = 1;
        dropTarget.style.border = "";

        openWindow(event, data);
    }
});