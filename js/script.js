function resizeToMinimum(w) {
    w = w > window.outerWidth ? w : window.outerWidth;
    window.resizeTo(w, window.outerHeight);
};
window.addEventListener("resize", function() {resizeToMinimum(650)}, false)