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

    function reveal(el) {
      el.classList.remove('scroll-trigger--offscreen');
      observer.unobserve(el);
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          // Scrolled clean past without ever intersecting: still reveal it,
          // or the element is stranded invisible above the viewport.
          if (!entry.isIntersecting && entry.boundingClientRect.bottom > 0) return;
          reveal(entry.target);
        });
      },
      { rootMargin: '0px 0px -50px 0px', threshold: 0 }
    );

    /* IntersectionObserver only fires on a *change* of intersection state. A
       jump that lands past an element — a hash link, a browser-restored scroll
       position, a full-page screenshot — moves it from "not intersecting,
       below" to "not intersecting, above" with no intersecting frame in
       between, so the callback never runs and the element keeps opacity 0
       forever. Three collection cards were permanently invisible this way.
       Sweeping on scroll costs one rAF per gesture and stops entirely once
       every target has been revealed. */
    var ticking = false;

    function sweep() {
      ticking = false;
      var left = document.querySelectorAll('.scroll-trigger--offscreen');
      for (var i = 0; i < left.length; i++) {
        if (left[i].getBoundingClientRect().bottom <= 0) reveal(left[i]);
      }
      if (!document.querySelector('.scroll-trigger--offscreen')) {
        window.removeEventListener('scroll', onScroll);
      }
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(sweep);
    }

    window.addEventListener('scroll', onScroll, { passive: true });

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
