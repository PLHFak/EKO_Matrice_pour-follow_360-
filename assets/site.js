(function () {
  var root = document.documentElement;

  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var dark = root.dataset.theme
        ? root.dataset.theme === 'dark'
        : window.matchMedia('(prefers-color-scheme: dark)').matches;
      var next = dark ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('eko-theme', next); } catch (e) {}
    });
  }

  var printBtn = document.getElementById('print');
  if (printBtn) {
    printBtn.addEventListener('click', function () { window.print(); });
  }

  // Highlight the section being read in the table of contents.
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var heads = Object.keys(byId).map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var current = null;
  function setActive(id) {
    if (id === current) return;
    if (current && byId[current]) byId[current].classList.remove('active');
    current = id;
    if (byId[id]) {
      byId[id].classList.add('active');
      byId[id].scrollIntoView({ block: 'nearest' });
    }
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) setActive(e.target.id); });
  }, { rootMargin: '-80px 0px -70% 0px' });
  heads.forEach(function (h) { observer.observe(h); });
})();
