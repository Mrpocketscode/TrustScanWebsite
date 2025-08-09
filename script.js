// Fade-in on scroll
const faders = document.querySelectorAll(
  '.feature-box, .hero-content, .about, .trust-coins, .contact, .coming-soon-content'
);
const appearOptions = { threshold: 0.2, rootMargin: '0px 0px -50px 0px' };
const appearOnScroll = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('appear');
    observer.unobserve(entry.target);
  });
}, appearOptions);
faders.forEach(el => appearOnScroll.observe(el));

// Mobile nav
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
}

// Simple scrollspy
const sections = document.querySelectorAll('main section[id]');
const links = document.querySelectorAll('.nav__link');
const spy = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const id = entry.target.id;
    links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === `#${id}`));
  });
}, { rootMargin: '-50% 0px -40% 0px' });
sections.forEach(s => spy.observe(s));
