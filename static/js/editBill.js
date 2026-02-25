const modal = document.querySelector("#editBillForm")

modal.addEventListener("submit", async (e) =>
{
    const form = e.target;
    console.log("submit")
    const response = await fetch(form.action, {method : "POST", body : new FormData(form)}) // havent got a fuckin clue tbh
})