/* ============================================================
   iSyslab site — shared components & behaviour
   Navbar + Footer are single-source (mirrors the design's
   reusable components: 3:2 Navbar, 3:16 Footer).
   Every label carries a data-i18n key resolved by assets/js/i18n.js.
   ============================================================ */

(function (w) {
  'use strict';

  /* 顶栏菜单：为控制宽度只保留一级栏目，「加入我们」作为 CTA 放在首页主视觉区
     （见 index.html 的 .cta-row）。News 已从顶栏与页脚移除、内容保留在
     news.html 与首页动态区；需要恢复到菜单时，把下面这行加回来即可：
     { k: 'nav.news', href: 'news.html' } */
  var NAV_LINKS = [
    { k: 'nav.home',     href: 'index.html' },
    { k: 'nav.research', href: 'research.html' },
    { k: 'nav.people',   href: 'people.html' },
    { k: 'nav.pubs',     href: 'publications.html' },
    { k: 'nav.patents',  href: 'patents.html' },
    { k: 'nav.software', href: 'software.html' },
    { k: 'nav.teaching', href: 'teaching.html' }
  ];

  function currentPage() {
    var p = location.pathname.split('/').pop();
    return p === '' ? 'index.html' : p;
  }

  function i(k) { return w.I18N ? w.I18N.t(k) : ''; }

  /* ---------- Navbar (design component 3:2) ---------- */
  function renderNavbar() {
    var host = document.getElementById('site-navbar');
    if (!host) return;
    var cur = currentPage();

    var links = NAV_LINKS.map(function (l) {
      var active = l.href === cur ? ' class="active"' : '';
      return '<a href="' + l.href + '"' + active + ' data-i18n="' + l.k + '">' + i(l.k) + '</a>';
    }).join('');

    host.innerHTML =
      '<div class="navbar">' +
        '<div class="navbar-inner">' +
          '<a class="brand" href="index.html" aria-label="iSyslab — Zhidong\'s Research Group at HUST">' +
            '<img class="brand-mark" src="assets/img/logo-mark.svg" alt="">' +
            '<span class="brand-text">' +
              '<span class="brand-name"><span class="wm-i">i</span>Syslab</span>' +
              '<span class="brand-sub" data-i18n="brand.sub">' + i('brand.sub') + '</span>' +
            '</span>' +
          '</a>' +
          '<nav class="nav-links">' + links + '</nav>' +
          '<div class="lang-switch" role="group" aria-label="Language / 语言">' +
            '<button type="button" class="lang-opt lang-en" data-lang-set="en" title="English">EN</button>' +
            '<button type="button" class="lang-opt lang-zh" data-lang-set="zh" title="切换到中文">中文</button>' +
          '</div>' +
        '</div>' +
      '</div>';
  }

  /* ---------- Footer (design component 3:16) ---------- */
  function renderFooter() {
    var host = document.getElementById('site-footer');
    if (!host) return;

    host.innerHTML =
      '<footer class="footer">' +
        '<div class="footer-inner">' +
          '<div class="footer-top">' +
            '<div class="footer-brand">' +
              '<div class="footer-lockup">' +
                '<img class="footer-mark" src="assets/img/logo-mark-reverse.svg" alt="">' +
                '<span class="footer-text">' +
                  '<span class="footer-name"><span class="wm-i">i</span>Syslab</span>' +
                  '<span class="footer-sub" data-i18n="brand.sub">' + i('brand.sub') + '</span>' +
                '</span>' +
              '</div>' +
              '<p data-i18n="footer.tagline" data-i18n-html>' + i('footer.tagline') + '</p>' +
            '</div>' +
            '<div class="footer-cols">' +
              '<div class="footer-col">' +
                '<h4 data-i18n="footer.site">' + i('footer.site') + '</h4>' +
                '<a href="index.html" data-i18n="nav.home">' + i('nav.home') + '</a>' +
                '<a href="research.html" data-i18n="nav.research">' + i('nav.research') + '</a>' +
                '<a href="people.html" data-i18n="nav.people">' + i('nav.people') + '</a>' +
                '<a href="publications.html" data-i18n="nav.pubs">' + i('nav.pubs') + '</a>' +
              '</div>' +
              '<div class="footer-col">' +
                '<h4 data-i18n="footer.explore">' + i('footer.explore') + '</h4>' +
                '<a href="software.html" data-i18n="nav.software">' + i('nav.software') + '</a>' +
                '<a href="patents.html" data-i18n="nav.patents">' + i('nav.patents') + '</a>' +
                '<a href="teaching.html" data-i18n="nav.teaching">' + i('nav.teaching') + '</a>' +
                '<a href="gallery.html" data-i18n="nav.gallery">' + i('nav.gallery') + '</a>' +
                '<a href="join.html" data-i18n="nav.join">' + i('nav.join') + '</a>' +
              '</div>' +
              '<div class="footer-col footer-col-contact">' +
                '<h4 data-i18n="footer.contact">' + i('footer.contact') + '</h4>' +
                '<a href="mailto:zdxue@hust.edu.cn">zdxue@hust.edu.cn</a>' +
                '<span data-i18n="footer.school">' + i('footer.school') + '</span>' +
                '<span data-i18n="footer.address">' + i('footer.address') + '</span>' +
                '<span data-i18n="footer.postcode">' + i('footer.postcode') + '</span>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="footer-bottom">' +
            '<span data-i18n="footer.copyright">' + i('footer.copyright') + '</span>' +
          '</div>' +
        '</div>' +
      '</footer>';
  }

  /* ---------- Publications / year filter ---------- */
  function initPubFilter() {
    var chips = document.querySelectorAll('.year-filter .chip');
    if (!chips.length) return;
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('active'); });
        chip.classList.add('active');
        var year = chip.getAttribute('data-year');
        document.querySelectorAll('.pub-group[data-year]').forEach(function (g) {
          g.style.display = (year === 'all' || g.getAttribute('data-year') === year) ? '' : 'none';
        });
      });
    });
  }

  function boot() {
    renderNavbar();
    renderFooter();
    initPubFilter();
    if (w.I18N) w.I18N.init();
  }

  /* This script sits at the end of <body>, so the DOM is already
     parsed — boot synchronously to avoid a flash of untranslated text. */
  boot();
})(window);
