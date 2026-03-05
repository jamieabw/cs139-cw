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
        if (!responseData.ok) {
            console.log(responseData.errors)
            for (error of responseData.errors) {
                document.querySelector(".errors").innerHTML = error
            }
            return;
        }
        // close the parent of the parent of the form (the modal by calling .hide())
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