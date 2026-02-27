const modal = document.querySelector("#editBillForm")



/**this is by far the worst thing i have ever programmed, it is 
 * COMPLETE spaghetti code and MUST be ammended before submission, this
 * is genuinely atrocious
 */
modal.addEventListener("submit",  async (e) =>
{
    console.log("submit");
    e.preventDefault(); // inorder to prevent the form from submitting again
    const form = e.target;
    const fd = new FormData(form); // stores the form data
    for (data in Object.fromEntries(fd.entries())) {
        console.log(data);
    }
    //console.log("next");
    const payload = Object.fromEntries(fd.entries()); 
    console.log(payload);
    const description = payload.description;
    const total = payload.total;
    console.log(description);
    console.log(total);
    
    //const response = await fetch(form.action, {method : "POST", body : new FormData(form)}) // havent got a fuckin clue tbh
    const response = await fetch(form.action, {method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({description : description, total: total})}); // sends a json of the updated bill details to updat the db with
    if (!response.ok) {
        console.log("error revolving getting form data")
        return
    }
    const responseData = await response.json();
    const billId = responseData.billId;
    console.log(billId);
    document.querySelectorAll(".paymentRow").forEach((row) => row.remove());
    const response2 = await fetch(`/group/bill/${billId}/debtorsData`);
    const responseData2 = await response2.json();
    const debtorsGrid = document.querySelector("#debtorsGrid");
    // resets the original debtorsGrid
    debtorsGrid.innerHTML = `<div class="row">
      <div class="col">Name</div>
      <div class="col">Proportion</div>
      <div class="col">Owed</div>
    </div>
  `;
  console.log("the debtors grid template has loaded")
    // generates the rows of the debtors to replace previous ones
    for (d of responseData2.debtors) {
        console.log("row starting")

        let row = document.createElement("div");
        row.className = "row"; // for bootstrap
        row.innerHTML = `
      <div class="col">${d.username}</div>
      <div class="col">${d.proportion}%</div>
      <div class="col">£${d.owed}</div>
    `;
    // need to fix bug with proportion and owed displaying differently (50, instead of 50.00), either is fine but needs to be consistent
    debtorsGrid.appendChild(row);
    }
})