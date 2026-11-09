(function () {
  var root = document.documentElement;
  var header = document.querySelector('.header');
  var toggle = document.querySelector('.menu-toggle');

  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
  // GA4: klikken op bellen / mailen meten
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="tel:"], a[href^="mailto:"]');
    if (!a || typeof window.gtag !== 'function') return;
    var tel = a.getAttribute('href').indexOf('tel:') === 0;
    window.gtag('event', tel ? 'phone_click' : 'email_click', {
      link_url: a.getAttribute('href'),
      link_text: (a.textContent || '').trim().slice(0, 60),
      page_location: location.href
    });
  });

  root.classList.add('js');
})();
