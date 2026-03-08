
/**
 * 
 * gets the sliders value and updates the label, then also updates the total percent too
 */
function update(slider) {
  const percentage = document.querySelector(`.percent[data-for="${slider.id}"]`);
  if (percentage) {
    percentage.textContent = slider.value;
  }
  let totalPercentage = 0;
  for (const percent of document.querySelectorAll(".percent")) {
    console.log(percent);
    totalPercentage += Number(percent.textContent);
  }
  console.log(totalPercentage);
  const totalPercentageSpan = document.querySelector(".totalPercent");
  totalPercentageSpan.textContent = "Total: " + totalPercentage;
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('input[type="range"]').forEach(update);
});

/**
 * self explanatory - sets the percents to split the debt evenly between all members
 */
function splitEvenly() {
    const count = document.querySelectorAll(".percent").length;
    const evenSplit = 100 / count;
    for (const slider of document.querySelectorAll('input[type="range"]')) {
        slider.value = evenSplit;
        update(slider);
    }


}
