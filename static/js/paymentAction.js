const paymentsGrid = document.querySelector(".paymentGrid");

paymentsGrid.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return; // button wasnt clicked on the payment grid
  const action = btn.dataset.action;
  const paymentId = btn.dataset.paymentId;

  //console.log("billId", billId);
  console.log("payment Id, action:", paymentId, action);
  const response = await fetch("/group/payment/action", {
    method: "POST",
    headers : {"Content-Type": "application/json"},
    body : JSON.stringify({paymentId : paymentId, action : action})
  }) // sends the json to the toute containing the payment id and action so the backend can deal with the action
  if (response.ok) {
    const row = btn.closest(".paymentRow");
    if (!row) {
        console.log("row not found");
        return;
    }
    // remove both the buttons
    row.querySelectorAll("button").forEach((button) => button.remove());

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