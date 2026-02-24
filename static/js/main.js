const debtsGrid = document.querySelector(".debtsGrid")
const popupForm = document.querySelector(".settleDebt");
const fieldToFill = document.querySelector("#billId")
/** Checks if the user has clicked the 'settle' button next to the debts. if it does, finds the assocaited
 * billId 
 */
debtsGrid.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-bill-id]");
  if (!btn) return;

  const billId = btn.dataset.billId; // JS converts the kebab case to camel case and removes the data- prefix apparently?
  //console.log("billId", billId);
  fieldToFill.value = billId
  console.log("billId", billId);
});
 // this does work but need to figure out why
