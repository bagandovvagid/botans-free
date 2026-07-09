/*
 * Тема сайта: светлые или тёмные обои. Меняются только обои,
 * весь остальной контент выглядит одинаково в обеих темах.
 *
 * Как выбирается тема при заходе:
 *   1) выбор пользователя, сохранённый после клика по переключателю;
 *   2) тема Telegram — когда сайт открыт как Mini App внутри Telegram;
 *   3) тема устройства (prefers-color-scheme).
 *
 * Подключается синхронно в <head>, чтобы нужные обои применились
 * до первой отрисовки — без «мигания» не той темы.
 */
(function () {
  var html = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function savedTheme() {
    try { return localStorage.getItem('theme'); } catch (e) { return null; }
  }

  function deviceDark() {
    var tg = window.Telegram && window.Telegram.WebApp;
    if (tg && tg.platform && tg.platform !== 'unknown' && tg.colorScheme) {
      return tg.colorScheme === 'dark';
    }
    return !!(media && media.matches);
  }

  function apply(dark) {
    html.classList.toggle('dark', dark);

    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.setAttribute('aria-checked', String(dark));
      btn.setAttribute('aria-label', dark ? 'Включить светлую тему' : 'Включить тёмную тему');
    }

    // Цвет интерфейса браузера на телефонах — под текущие обои
    var metas = document.querySelectorAll('meta[name="theme-color"]');
    for (var i = 0; i < metas.length; i++) {
      metas[i].setAttribute('content', dark ? '#101b13' : '#6eb075');
    }

    try {
      document.dispatchEvent(new CustomEvent('bf:themechange', { detail: { dark: dark } }));
    } catch (e) {}
  }

  // Доступно другим скриптам: tg.js по этому API красит шапку Telegram
  window.siteTheme = {
    apply: apply,
    saved: savedTheme,
    isDark: function () { return html.classList.contains('dark'); }
  };

  // Применяем тему сразу, до отрисовки страницы
  apply(savedTheme() ? savedTheme() === 'dark' : deviceDark());

  // Пока пользователь не выбрал тему вручную — следуем за темой устройства,
  // в том числе если она сменилась прямо во время просмотра
  if (media) {
    var follow = function (e) { if (!savedTheme()) apply(e.matches); };
    if (media.addEventListener) media.addEventListener('change', follow);
    else if (media.addListener) media.addListener(follow);
  }

  // Кнопка-ползунок: клик переключает тему и запоминает выбор
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.setAttribute('aria-checked', String(html.classList.contains('dark')));
    btn.addEventListener('click', function () {
      var dark = !html.classList.contains('dark');
      try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
      apply(dark);
    });
  });

  // После полной загрузки тихо докачиваем обои второй темы,
  // чтобы переключение было мгновенным, без белой вспышки
  window.addEventListener('load', function () {
    setTimeout(function () { html.classList.add('wp-armed'); }, 500);
  });
})();
