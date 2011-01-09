(function () {
    var b = document.createElement("script");
    b.type = "text/javascript";
    b.src = "http://mathjax.connectmv.com/MathJax.js";
    var a = 'MathJax.Hub.Config({extensions: ["tex2jax.js", "TeX/AMSmath.js", "TeX/noUndefined.js", "TeX/AMSsymbols.js"],"HTML-CSS": { preferredFont: "TeX", imageFont: null, availableFonts: ["STIX","TeX"], webFont: "TeX" },jax: ["input/TeX","output/HTML-CSS"],TeX: { noUndefined: { attributes: { mathcolor: "red", mathbackground: "#FFEEEE", mathsize: "90%" } } }});MathJax.Hub.Startup.onload();';
    if (window.opera) {
        b.innerHTML = a
    } else {
        b.text = a
    }
    document.getElementsByTagName("head")[0].appendChild(b)
})();