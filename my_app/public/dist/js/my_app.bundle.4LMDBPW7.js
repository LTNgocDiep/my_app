(()=>{function o(){$(".group-by-item").each(function(){var n,a;let e=$(this),t=decodeURIComponent(e.attr("data-value")||"");if(!t.includes("@"))return;let i=((a=(n=frappe.boot.user_info)==null?void 0:n[t])==null?void 0:a.fullname)||t;e.find(".group-by-value").text(i)})}requestAnimationFrame(function e(){o(),requestAnimationFrame(e)});})();
//# sourceMappingURL=my_app.bundle.4LMDBPW7.js.map
