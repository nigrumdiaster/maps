// static/js/plugins.js
(function() {
    function loadScript(src, async = true, defer = false) {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = src;
        script.async = async;
        script.defer = defer;
        document.head.appendChild(script);
    }

    document.addEventListener('DOMContentLoaded', function() {
        if (document.querySelector("[toast-list]") || document.querySelector("[data-choices]") || document.querySelector("[data-provider]")) {
            loadScript('https://cdn.jsdelivr.net/npm/toastify-js', true, true);
            loadScript('/static/assets/libs/choices.js/public/assets/scripts/choices.min.js', true, true);
            loadScript('/static/assets/libs/flatpickr/flatpickr.min.js', true, true);
        }
    });
})();
