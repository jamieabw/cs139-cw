const modal = document.querySelector("#editBillForm")

modal.addEventListener("submit", async (e) =>
{
  e.preventDefault();
  const form = e.target;
  const response = await fetch(form.action, {
    method: "POST",
    body: new FormData(form)
  });
  const responseData = await response.json();
  if (!responseData.ok) {
    console.log("error", responseData);
  }
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