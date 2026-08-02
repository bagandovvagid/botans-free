/*
 * Общее поведение всех страниц Luxury Edition:
 * мобильное меню, аккордеоны и уведомление на кнопках входа.
 *
 * Всё на делегировании событий: страницы статичные, отдельных скриптов
 * под каждую заводить незачем.
 */
(function () {
  'use strict';

  // ===== Переключатель темы =====
  // Само применение темы уже произошло раньше, в assets/theme-init.js
  // (до отрисовки, чтобы не мигало). Здесь только иконка и клик.
  var themeBtn = document.getElementById('theme-toggle');
  var ICON_SUN = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
  var ICON_MOON = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  function isLight() { return document.documentElement.getAttribute('data-theme') === 'light'; }

  function paintThemeBtn() {
    if (!themeBtn) return;
    // Показываем иконку того, во что переключит клик, а не текущего состояния
    themeBtn.innerHTML = isLight() ? ICON_MOON : ICON_SUN;
    themeBtn.setAttribute('aria-label', isLight() ? 'Включить тёмную тему' : 'Включить светлую тему');
  }

  if (themeBtn) {
    paintThemeBtn();
    themeBtn.addEventListener('click', function () {
      var light = !isLight();
      document.documentElement.setAttribute('data-theme', light ? 'light' : 'dark');
      try { localStorage.setItem('bf-theme', light ? 'light' : 'dark'); } catch (e) {}

      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', light ? '#f7f6f4' : '#0a0a0b');

      paintThemeBtn();
    });
  }

  // ===== Мобильное меню =====
  var burger = document.querySelector('.nav-burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
  }

  // ===== Аккордеон =====
  // Высоту берём из содержимого: max-height анимируется, auto — нет.
  document.addEventListener('click', function (e) {
    var q = e.target.closest ? e.target.closest('.acc-q') : null;
    if (!q) return;

    var item = q.parentNode;
    var panel = item.querySelector('.acc-a');
    var open = item.classList.toggle('is-open');

    q.setAttribute('aria-expanded', String(open));
    panel.style.maxHeight = open ? panel.scrollHeight + 'px' : '';
  });

  // ===== Уведомление =====
  var toast = document.getElementById('toast');
  var hideTimer = null;

  function say(text) {
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add('is-on');
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function () { toast.classList.remove('is-on'); }, 3600);
  }

  // Вход и регистрация нарисованы, но аккаунтов на сайте пока нет —
  // заказы принимаются в Telegram. Кнопка честно про это говорит.
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-soon]') : null;
    if (!el) return;
    e.preventDefault();
    say(el.getAttribute('data-soon') || 'Скоро добавим');
  });

  // ===== Форма обращения =====
  // Отправлять её пока некуда: бэкенда у сайта нет. Чтобы письмо не
  // потерялось молча, отправляем человека в Telegram.
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      say('Форма ещё не подключена — напишите, пожалуйста, в Telegram @botans_free');
    });
  }
})();
