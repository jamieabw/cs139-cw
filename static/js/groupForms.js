//var modalForm = document.querySelector(".createGroupForm")
document.querySelectorAll(".groupForm").forEach((formEl) => {
    formEl.addEventListener("submit", async (e) => {
        e.preventDefault();
        form = e.target;
        const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form)
    });
        const responseData = await response.json();
        if (!responseData.ok) {const modalForm = document.querySelector(".joinGroupForm")
    modalForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        form = e.target;
        const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form)
    });
        const responseData = await response.json();
        if (!responseData.ok) {
            console.log("error")
            return;
        }
        const groupGrid = document.querySelector(".groupGrid");
        if (!groupGrid) {
            return; // not on index
        }
        const row = document.createElement("div");
        row.className = "row groupContainer";
        row.innerHTML = `<a href=${responseData.groupUrl}>
                <div class="col">${responseData.groupName}</div>
                <div class="col">${responseData.groupId}</div>
                <div class="col">${responseData.groupCreatedAt}</div>
                </a>`


        groupGrid.appendChild(row);

    })
            console.log("error")
            return;
        }
        const groupGrid = document.querySelector(".groupGrid");
        if (!groupGrid) {
            return; // not on index
        }
        const row = document.createElement("div");
        row.className = "row groupContainer";
        row.innerHTML = `<a href=${responseData.groupUrl}>
                <div class="col">${responseData.groupName}</div>
                <div class="col">${responseData.groupId}</div>
                <div class="col">${responseData.groupCreatedAt}</div>
                </a>`


        groupGrid.appendChild(row);

    })
})