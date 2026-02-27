const debtsGrid = document.querySelector(".debtsGrid")
const popupForm = document.querySelector(".settleDebt");
const fieldToFill = document.querySelector("#billId")
/** Checks if the user has clicked the 'settle' button next to the debts. if it does, finds the assocaited
 * billId and fills in the form with it
 */
debtsGrid.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-bill-id]");
  if (!btn) return;

  const billId = btn.dataset.billId;
  fieldToFill.value = billId
  console.log("billId", billId);
});
