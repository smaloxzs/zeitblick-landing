"use strict";

/* Banner oben: einmal geschlossen, bleibt es fuer diesen Browser zu */
const topBanner = document.getElementById("topBanner");
const topBannerClose = document.getElementById("topBannerClose");
if (topBanner && topBannerClose) {
  try {
    if (localStorage.getItem("zeitblick.bannerClosed") === "1") {
      topBanner.style.display = "none";
    }
  } catch (e) {}
  topBannerClose.addEventListener("click", () => {
    topBanner.style.display = "none";
    try { localStorage.setItem("zeitblick.bannerClosed", "1"); } catch (e) {}
  });
}

/* Mobiles Menü */
const navToggle = document.getElementById("navToggle");
const mainNav = document.getElementById("mainNav");
if (navToggle && mainNav) {
  navToggle.addEventListener("click", () => {
    const open = mainNav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(open));
  });
  mainNav.querySelectorAll("a").forEach(a =>
    a.addEventListener("click", () => {
      mainNav.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    })
  );
}

