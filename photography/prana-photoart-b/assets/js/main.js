/* Shared helpers: active nav + portfolio filter + lightbox */
(function () {
  // Active nav link by current page
  const path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  document.querySelectorAll(".navlinks a").forEach(a => {
    const href = (a.getAttribute("href") || "").toLowerCase();
    if (href === path) a.classList.add("active");
    if (path === "" && href === "index.html") a.classList.add("active");
  });

  // Lightbox
  const lb = document.querySelector(".lightbox");
  const lbImg = document.querySelector(".lightbox img");
  const lbCap = document.querySelector("[data-lightbox-caption]");
  const closeBtn = document.querySelector(".lightbox-close");

  function openLightbox(src, caption){
    if (!lb || !lbImg) return;
    lbImg.src = src;
    if (lbCap) lbCap.textContent = caption || "";
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeLightbox(){
    if (!lb) return;
    lb.classList.remove("open");
    document.body.style.overflow = "";
    if (lbImg) lbImg.src = "";
  }

  document.querySelectorAll("[data-lightbox]").forEach(el => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const src = el.getAttribute("data-src") || el.getAttribute("href");
      const cap = el.getAttribute("data-caption") || "";
      openLightbox(src, cap);
    });
  });

  if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
  if (lb) {
    lb.addEventListener("click", (e) => { if (e.target === lb) closeLightbox(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeLightbox(); });
  }

  // Filters (portfolio page)
  const chips = document.querySelectorAll("[data-filter]");
  const items = document.querySelectorAll("[data-category]");
  if (chips.length && items.length){
    chips.forEach(chip => {
      chip.addEventListener("click", () => {
        chips.forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        const val = chip.getAttribute("data-filter");
        items.forEach(it => {
          const cat = it.getAttribute("data-category") || "";
          it.style.display = (val === "all" || cat.includes(val)) ? "" : "none";
        });
      });
    });
  }

  // “Print” buttons on Documents page
  document.querySelectorAll("[data-print]").forEach(btn => {
    btn.addEventListener("click", () => window.print());
  });
})();
