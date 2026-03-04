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

  // --- Mobile Menu (JS toggle instead of checkbox hack) ---
  const hamburger = document.querySelector('.nav__hamburger');
  const navLinksContainer = document.querySelector('.nav__links');

  if (hamburger && navLinksContainer) {
    hamburger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = navLinksContainer.classList.toggle('nav__links--open');
      hamburger.classList.toggle('nav__hamburger--open', isOpen);
    });

    // Close on nav link click
    navLinksContainer.querySelectorAll('.nav__link').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinksContainer.classList.remove('nav__links--open');
        hamburger.classList.remove('nav__hamburger--open');
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (navLinksContainer.classList.contains('nav__links--open')) {
        if (!e.target.closest('.nav__links') && !e.target.closest('.nav__hamburger')) {
          navLinksContainer.classList.remove('nav__links--open');
          hamburger.classList.remove('nav__hamburger--open');
        }
      }
    });
  }

  // --- Active Page Highlighting ---
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__link').forEach(function (link) {
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
