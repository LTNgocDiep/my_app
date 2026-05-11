(()=>{console.log("PATCH LOADED");function a(){$(".group-by-item").each(function(){var l,n;let t=$(this),e=decodeURIComponent(t.attr("data-value")||"");if(!e.includes("@"))return;let o=((n=(l=frappe.boot.user_info)==null?void 0:l[e])==null?void 0:n.fullname)||e;t.find(".group-by-value").text(o)})}setInterval(()=>{a()},500);})();
//# sourceMappingURL=my_app.bundle.LOIUDSTZ.js.map
