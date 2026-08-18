/* JJW theme behaviour.
   Converted from the React codebase's ScrollReveal component: elements marked
   .scroll-trigger start with .scroll-trigger--offscreen and have it removed
   once they enter the viewport, which is what fires the CSS animation. */

(function () {
  'use strict';

  function initScrollReveal() {
    var targets = document.querySelectorAll('.scroll-trigger');
    if (!targets.length) return;

    // No IntersectionObserver, or the visitor prefers reduced motion:
    // show everything immediately rather than leaving it invisible.
    if (
      !('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ) {
      targets.forEach(function (el) {
        el.classList.remove('scroll-trigger--offscreen');
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.remove('scroll-trigger--offscreen');
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -50px 0px', threshold: 0 }
    );

    targets.forEach(function (el) {
      el.classList.add('scroll-trigger--offscreen');
      observer.observe(el);
    });
  }

  function init() {
    initScrollReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Shopify theme editor re-renders sections without a page reload.
  document.addEventListener('shopify:section:load', init);
})();
