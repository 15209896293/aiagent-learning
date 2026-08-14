/* VibeHub 课程站 · 明暗主题切换（与主站一致） */
(function () {
  var key = "vh_theme";
  var saved = localStorage.getItem(key) || "light";
  var root = document.documentElement;
  root.setAttribute("data-theme", saved);
  var btn = document.getElementById("themeBtn");
  function paint() {
    if (!btn) return;
    var dark = root.getAttribute("data-theme") === "dark";
    var moon = btn.querySelector(".i-moon");
    var sun = btn.querySelector(".i-sun");
    if (moon) moon.hidden = dark;
    if (sun) sun.hidden = !dark;
    btn.title = "切换主题";
  }
  if (btn) {
    btn.onclick = function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem(key, next);
      paint();
    };
  }
  paint();
})();
