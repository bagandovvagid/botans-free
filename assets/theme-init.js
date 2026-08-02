/*
 * Применяет сохранённую тему ДО отрисовки страницы — чтобы не было вспышки
 * не той темы. Поэтому подключается блокирующим <script src> в начале
 * <head>, а не в конце body вместе с остальным поведением (luxury.js).
 *
 * Тёмная тема — значения по умолчанию в :root, светлая — переопределение
 * через :root[data-theme="light"]. Значит по умолчанию ничего делать не
 * нужно: атрибут выставляется только когда нужна светлая версия.
 */
(function () {
  try {
    var saved = localStorage.getItem('bf-theme');
    var wantLight = saved ? saved === 'light'
      : (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches);

    if (wantLight) {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  } catch (e) {}
})();
