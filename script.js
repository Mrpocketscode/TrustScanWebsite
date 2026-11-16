/* Trust Scan+ landing site script.
   Loaded as an external file because the CSP is script-src 'self' (no inline JS). */

/* -------------------------------------------------------------
   APP STORE LINKS: the one place to update when the app ships.
   Leave a value as null to keep sending that button to the
   coming-soon page. Example:
     ios: "https://apps.apple.com/app/idXXXXXXXXX",
     android: "https://play.google.com/store/apps/details?id=com.example"
   Store pages are links, not embeds, so the CSP needs no change.
------------------------------------------------------------- */
var STORE_LINKS = {
  ios: null,
  android: null
};

(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.remove("no-js");

  /* A new page always opens at the top. Back and forward still return to
     where you were, and links to a section (#faq) still jump to it. */
  function toTop() {
    var nav = window.performance && performance.getEntriesByType &&
      performance.getEntriesByType("navigation")[0];
    var fresh = !nav || nav.type === "navigate";
    if (fresh && !location.hash) window.scrollTo(0, 0);
  }
  toTop();
  window.addEventListener("load", toTop);

  document.addEventListener("DOMContentLoaded", function () {
    /* Mobile navigation */
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        toggle.textContent = open ? "Close" : "Menu";
      });
      nav.addEventListener("click", function (e) {
        if (e.target.closest("a") && nav.classList.contains("open")) {
          nav.classList.remove("open");
          toggle.setAttribute("aria-expanded", "false");
          toggle.textContent = "Menu";
        }
      });
    }

    /* Store buttons on the coming-soon page */
    document.querySelectorAll("[data-store]").forEach(function (btn) {
      var url = STORE_LINKS[btn.getAttribute("data-store")];
      if (url) {
        btn.setAttribute("href", url);
        btn.removeAttribute("aria-disabled");
        btn.setAttribute("rel", "noopener");
        var note = btn.querySelector("small");
        if (note) note.textContent = "Available now";
      }
    });

    /* "Get the app" buttons ([data-app-link]) always go to
       coming-soon.html. Once STORE_LINKS is filled in, that page
       shows live store buttons, so these need no change. */

    /* Animated mascots: respect reduced motion and pause off-screen */
    var videos = Array.prototype.slice.call(document.querySelectorAll("video"));
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduce) {
      videos.forEach(function (v) {
        v.removeAttribute("autoplay");
        v.pause();
      });
    } else if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          var v = entry.target;
          if (entry.isIntersecting) {
            var p = v.play();
            if (p && p.catch) p.catch(function () {});
          } else {
            v.pause();
          }
        });
      }, { threshold: 0.15 });
      videos.forEach(function (v) { io.observe(v); });
    }

    /* Old single-page links (trustscanapp.com/#pricing) go to the new pages */
    var moved = {
      "#how": "how-it-works.html", "#engine": "how-it-works.html", "#verify": "how-it-works.html#verify",
      "#report": "example-report.html", "#monitoring": "monitoring.html",
      "#pricing": "pricing.html", "#limits": "pricing.html#limits", "#faq": "faq.html"
    };
    var path = location.pathname;
    if ((path === "/" || /\/index\.html$/.test(path)) && moved[location.hash] &&
        !document.getElementById(location.hash.slice(1))) {
      location.replace(moved[location.hash]);
      return;
    }

    /* Footer year */
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  });
})();
