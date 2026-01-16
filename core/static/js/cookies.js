document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("accept-cookies");
  const rejectBtn = document.getElementById("reject-cookies");
  const preferencesBtn = document.getElementById("preferences-cookies");
  const modal = document.getElementById("cookie-modal");
  const form = document.getElementById("cookie-preferences-form");
  const closeBtn = document.getElementById("close-cookie-modal");
  const manageLink = document.getElementById("manage-cookies");
  const reopenLink = document.getElementById("reopen-preferences");


  if (!getCookie("cookiesChoice")) {
    banner.style.display = "block";
  } else {
    banner.style.display = "none";
  }

  //acceptBtn.addEventListener("click", function () {
    //localStorage.setItem("cookiesChoice", JSON.stringify({
  document.getElementById("accept-cookies").addEventListener("click", function () {
    setCookie("cookiesChoice", JSON.stringify({
      functional: true,
      analytics: true,
      marketing: true
    }), 180);
    banner.style.display = "none";
    loadAnalytics();
    loadMarketing();
  });

    // Manage Cookies → reopen banner
    manageLink.addEventListener("click", function (e) {
      e.preventDefault();
      banner.style.display = "block";
    });
  
    // Reopen Preferences → open modal directly
    reopenLink.addEventListener("click", function (e) {
      e.preventDefault();
      modal.style.display = "block";
    });
  

  //rejectBtn.addEventListener("click", function () {
    //localStorage.setItem("cookiesChoice", JSON.stringify({
  document.getElementById("reject-cookies").addEventListener("click", function () {
    setCookie("cookiesChoice", JSON.stringify({
      functional: true,
      analytics: false,
      marketing: false
    }), 180);
    banner.style.display = "none";
  });

  preferencesBtn.addEventListener("click", function () {
    modal.style.display = "block";
  });

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const prefs = {
      functional: true,
      analytics: document.getElementById("analytics-cookies").checked,
      marketing: document.getElementById("marketing-cookies").checked
    };
    setCookie("cookiesChoice", JSON.stringify(prefs), 180);
    modal.style.display = "none";
    banner.style.display = "none";

    if (prefs.analytics) loadAnalytics();
    if (prefs.marketing) loadMarketing();
  });

  // Load scripts if already accepted
  const savedPrefs = JSON.parse(getCookie("cookiesChoice") || "{}");
  if (savedPrefs.analytics) loadAnalytics();
  if (savedPrefs.marketing) loadMarketing();
});

  // Close modal without saving
  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

// Optional: close if user clicks outside modal
  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });

// Example functions
function loadAnalytics() {
  const scriptTag = document.createElement("script");
  scriptTag.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"; // replace with GA ID
  scriptTag.async = true;
  document.head.appendChild(scriptTag);

  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag("js", new Date());
  gtag("config", "G-XXXXXXX"); // replace with GA ID
}

function loadMarketing() {
  // Example: Facebook Pixel or other marketing script
  console.log("Marketing cookies enabled");
}

// cookies helper
function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days*24*60*60*1000));
    expires = "; expires=" + date.toUTCString();

  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";

}

function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(';');
  for(let i=0;i < ca.length;i++) {
    let c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);

  }
  return null;
}



//document.addEventListener("DOMContentLoaded", function () {
    //const banner = document.getElementById("cookie-banner");
    //const acceptBtn = document.getElementById("accept-cookies");
    //const rejectBtn = document.getElementById("reject-cookies");

    // Show banner if no choice yet
    //if (!localStorage.getItem("cookiesChoice")) {
      //banner.style.display = "block";
    //}

    // Accept cookies
    //acceptBtn.addEventListener("click", function () {
      //localStorage.setItem("cookiesChoice", "accepted");
      //banner.style.display = "none";
      //loadAnalytics(); // ✅ load GA only if accepted
    //});

    // Reject cookies
    //rejectBtn.addEventListener("click", function () {
      //localStorage.setItem("cookiesChoice", "rejected");
      //banner.style.display = "none";
      // ❌ do not load analytics
    //});

    // If already accepted, load analytics immediately
    //if (localStorage.getItem("cookiesChoice") === "accepted") {
      //loadAnalytics();
    //}
  //});

  // Function to load Google Analytics dynamically
  //function loadAnalytics() {
    // Example: Google Analytics 4
    //const scriptTag = document.createElement("script");
    //scriptTag.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"; // replace with your GA ID
    //scriptTag.async = true;
    //document.head.appendChild(scriptTag);

    //window.dataLayer = window.dataLayer || [];
    //function gtag(){dataLayer.push(arguments);}
    //gtag("js", new Date());
    //gtag("config", "G-XXXXXXX"); // replace with your GA ID
  //}//

