/* ==========================================================================
   toN0tErr — Shared JavaScript
   ========================================================================== */

(function () {
  'use strict';

  // --- Navigation Scroll Effect ---
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }

  // --- Mobile Menu ---
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.querySelectorAll('.nav__link');

  // Close mobile menu on link click
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      if (toggle) toggle.checked = false;
    });
  });

  // Close mobile menu on outside click
  document.addEventListener('click', function (e) {
    if (toggle && toggle.checked) {
      const isMenu = e.target.closest('.nav__links');
      const isHamburger = e.target.closest('.nav__hamburger');
      if (!isMenu && !isHamburger) {
        toggle.checked = false;
      }
    }
  });

  // --- Active Page Highlighting ---
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // --- Scroll Reveal (IntersectionObserver) ---
  var revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length > 0 && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all
    revealElements.forEach(function (el) {
      el.classList.add('visible');
    });
  }

})();
