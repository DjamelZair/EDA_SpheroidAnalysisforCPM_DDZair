/* ─── CLL Spheroid EDA — Shared UI components ────────────────────────────────
   Loaded by every page in docs/.
   Provides: collapsible cards, mobile sidebar, active nav highlight.
──────────────────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  /* ── Collapsible section cards ──────────────────────────────────────────── */
  function initCollapsible() {
    document.querySelectorAll('.sc-header').forEach(function (header) {
      header.addEventListener('click', function () {
        var card = this.closest('.section-card');
        if (card) card.classList.toggle('collapsed');
      });
    });
  }

  /* ── Mobile sidebar toggle ──────────────────────────────────────────────── */
  function initSidebar() {
    var sidebar  = document.getElementById('sidebar');
    var overlay  = document.getElementById('sidebar-overlay');
    var hamburger = document.getElementById('hamburger');

    if (!sidebar) return;

    function open() {
      sidebar.classList.add('sb-open');
      if (overlay) overlay.classList.add('visible');
    }
    function close() {
      sidebar.classList.remove('sb-open');
      if (overlay) overlay.classList.remove('visible');
    }

    if (hamburger) hamburger.addEventListener('click', function () {
      sidebar.classList.contains('sb-open') ? close() : open();
    });
    if (overlay) overlay.addEventListener('click', close);

    // Close sidebar when a nav link is tapped on mobile
    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 680) close();
      });
    });
  }

  /* ── Active nav highlight (highlight link whose anchor is in view) ──────── */
  function initActiveNav() {
    var links = Array.from(document.querySelectorAll('#sidebar a[href^="#"]'));
    if (!links.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          links.forEach(function (l) { l.classList.remove('active'); });
          var active = links.find(function (l) {
            return l.getAttribute('href') === '#' + id;
          });
          if (active) active.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

    document.querySelectorAll('[id]').forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ── Boot ───────────────────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    initCollapsible();
    initSidebar();
    initActiveNav();
  });
})();
