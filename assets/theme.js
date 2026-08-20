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

  /* Prefix matching for every search form on the site.

     Shopify's documented `options[prefix]=last` measurably does nothing on
     this store — /search?q=adven&options[prefix]=last returns 0 while
     /search?q=adven* returns 4. So the wildcard goes on at submit time
     instead. Sections echo the terms back through `remove_last: '*'`, so the
     star never shows up in the heading or the field.

     Bound to form[role="search"] rather than to a specific form, so the
     header drawer and the results page share the one rule. */
  function initSearchPrefix() {
    document.querySelectorAll('form[role="search"]').forEach(function (form) {
      if (form.dataset.prefixBound === '1') return;
      form.dataset.prefixBound = '1';

      form.addEventListener('submit', function () {
        var field = form.querySelector('input[name="q"]');
        if (!field) return;
        var term = field.value.trim();
        if (term === '' || term.slice(-1) === '*') return;
        field.value = term + '*';
      });
    });
  }

  function init() {
    initScrollReveal();
    initSearchPrefix();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Shopify theme editor re-renders sections without a page reload.
  document.addEventListener('shopify:section:load', init);
})();
