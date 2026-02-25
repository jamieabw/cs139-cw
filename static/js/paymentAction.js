const paymentsGrid = document.querySelector(".paymentGrid");

paymentsGrid.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  const action = btn.dataset.action;
  const paymentId = btn.dataset.paymentId;

  //console.log("billId", billId);
  console.log("payment Id, action:", paymentId, action);
  const response = await fetch("/group/payment/action", {
    method: "POST",
    headers : {"Content-Type": "application/json"},
    body : JSON.stringify({paymentId : paymentId, action : action})
  })
  if (response.ok) {
    // need to remove the buttons here then change status to whatever it should be
    const row = btn.closest(".paymentRow");
    if (!row) {
        console.log("row not found");
        return;
    }
    // remove both the buttons
    row.querySelector("button").remove();
    row.querySelector("button").remove();
    if (action == "ack") {
        row.querySelector(".status").textContent = "Acknowledged";
    }
    else {
        row.querySelector(".status").textContent = "Rejected";

    }

    return;
  }
  else {
    console.log("error found");
    console.log(response)
  }
});