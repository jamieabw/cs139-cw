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
                document.querySelectorAll(".errors").forEach((errorDiv) => {
                    errorDiv.innerHTML = error;
                })
            }
            return;
        }
        document.querySelectorAll(".modal").forEach((m) => {
            bootstrap.Modal.getInstance(m)?.hide();
        })
        const groupGrid = document.querySelector(".groupGrid");
        document.querySelector(".noGroupLabel")?.remove();
        if (!groupGrid) {
            return; // not on index
        }
        // add the new group to the group grid
        const row = document.createElement("div");
        row.innerHTML = `<a href="${responseData.groupUrl}">
                        <div class="text-wrap"><h3>${responseData.groupName}</h3></div>
                        <div><p class="mb-0">${responseData.groupCreatedAt}</p></div>
                        </a>`;
        row.className = "groupContainer bg-dark rounded d-flex justify-content-center flex-wrap text-nowrap-no";
        groupGrid.appendChild(row);

    })
})