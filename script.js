"use strict";

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

/* Waitlist-Formular: kein Backend vorhanden, öffnet stattdessen eine
   vorausgefüllte E-Mail. Die Adresse verlässt den Browser nirgendwo sonst hin. */
const waitlistForm = document.getElementById("waitlistForm");
if (waitlistForm) {
  waitlistForm.addEventListener("submit", e => {
    e.preventDefault();
    const email = document.getElementById("waitlistEmail").value.trim();
    const subject = encodeURIComponent("Zeitblick Early Access");
    const body = encodeURIComponent(
      `Hallo,\n\nich möchte gerne einen Platz im Zeitblick Early Access sichern.\n\nMeine E-Mail: ${email}\n`
    );
    window.location.href = `mailto:smalox.der.beste@gmail.com?subject=${subject}&body=${body}`;
    const note = document.getElementById("waitlistNote");
    if (note) note.textContent = "Dein E-Mail-Programm öffnet sich gleich mit einer vorausgefüllten Nachricht.";
  });
}
