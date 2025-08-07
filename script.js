// === Smooth Scroll Fade-in Animation ===
const faders = document.querySelectorAll('.feature-box, .hero-content, .about, .trust-coins, .contact, .coming-soon-content');

const appearOptions = {
  threshold: 0.2,
  rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;

    entry.target.classList.add("appear");
    observer.unobserve(entry.target);
  });
}, appearOptions);

faders.forEach(fader => {
  appearOnScroll.observe(fader);
});

// === Optional: Mobile Menu Toggle (If You Add a Burger Menu Later) ===
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.navbar ul');

if (navToggle) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}
