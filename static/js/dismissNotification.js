const notiSection = document.querySelector(".notificationSection");
notiSection.addEventListener("click", async (e) => {
    const btn = e.target.closest("button");
    if (!btn) {
        return;
    }
    const notificationId = btn.dataset.notificationId;
    console.log(notificationId);
    const response = await fetch("/notification/dismiss", {
    method: "POST",
    headers : {"Content-Type": "application/json"},
    body : JSON.stringify({notificationId : notificationId})
  }); // sends to backen to get rid of noti
    if (!response.ok) {
        console.log("error dismissing noti");
        return;
    }
    const responseData = await response.json();
    btn.parentElement.remove(); // delete the button + its span el
    if (responseData.numOfNotis == 0) {
        console.log("no notis left");
        notiSection.innerHTML = `
        <span class="dropdown-item text-wrap">You currently have no notifications.</span>
        `;
    }
    const notiCounter = document.querySelector(".notificationCounter");
    notiCounter.innerHTML = responseData.numOfNotis;
    return;


})