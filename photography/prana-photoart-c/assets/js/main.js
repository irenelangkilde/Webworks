(function(){
  const path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  document.querySelectorAll(".navlinks a").forEach(a=>{
    const href=(a.getAttribute("href")||"").toLowerCase();
    if(href===path) a.classList.add("active");
  });
  const yearEl=document.getElementById("year");
  if(yearEl) yearEl.textContent = new Date().getFullYear();
})();
