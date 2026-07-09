/*
 * Интеграция с Telegram Mini App.
 * Работает только когда страница открыта ВНУТРИ Telegram.
 * В обычном браузере ничего не меняет — ссылки и вёрстка работают как есть.
 */
(function () {
  var tg = window.Telegram && window.Telegram.WebApp;

  // Открыто ли реально внутри Telegram (а не просто загружен SDK в браузере)
  var inTelegram = !!(tg && tg.platform && tg.platform !== 'unknown');

  if (!inTelegram) return;

  // Помечаем <html>, чтобы при желании поправить вёрстку под Telegram через CSS
  document.documentElement.classList.add('in-telegram');

  // Готовность и разворот на весь экран
  try { tg.ready(); } catch (e) {}
  try { tg.expand(); } catch (e) {}

  // Длинную страницу удобнее скроллить, если свайп вниз не закрывает приложение
  try { tg.disableVerticalSwipes && tg.disableVerticalSwipes(); } catch (e) {}

  // Цвет шапки и фона под текущую тему сайта: светлые или тёмные обои
  function syncTelegramColors() {
    var dark = document.documentElement.classList.contains('dark');
    var color = dark ? '#101b13' : '#6eb075';
    try { tg.setHeaderColor && tg.setHeaderColor(color); } catch (e) {}
    try { tg.setBackgroundColor && tg.setBackgroundColor(color); } catch (e) {}
  }
  syncTelegramColors();
  document.addEventListener('bf:themechange', syncTelegramColors);

  // Пользователь сменил тему в самом Telegram: если тема сайта вручную
  // не выбиралась — следуем за Telegram
  try {
    tg.onEvent && tg.onEvent('themeChanged', function () {
      var t = window.siteTheme;
      if (t && !t.saved()) t.apply(tg.colorScheme === 'dark');
    });
  } catch (e) {}

  // Ссылки на Telegram (t.me) открываем нативно — внутри самого Telegram,
  // а не во встроенном браузере. Работает и для ссылок, добавленных скриптом,
  // потому что слушаем клики на всём документе.
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href) return;

    if (/^https?:\/\/t\.me\//i.test(href)) {
      ev.preventDefault();
      try { tg.openTelegramLink(href); } catch (e) { tg.openLink(href); }
    } else if (/^https?:\/\//i.test(href) && a.target === '_blank') {
      // Прочие внешние ссылки — во встроенном браузере Telegram
      ev.preventDefault();
      try { tg.openLink(href); } catch (e) {}
    }
    // Внутренние ссылки (bot.html, якоря) — обычное поведение, не трогаем
  }, false);
})();
