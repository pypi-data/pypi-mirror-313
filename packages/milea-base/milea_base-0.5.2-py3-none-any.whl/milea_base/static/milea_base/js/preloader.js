// Hide preloader when page loaded
window.onload = function () {
    var preloader = document.getElementById('preloader');
    preloader.style.display = 'none';
};

// Funktion, um den Preloader dyanmisch anzuzeigen
function showPreloader() {
    var preloader = document.getElementById('preloader');
    preloader.style.display = 'flex';
}

// Event Listener für alle Links und Buttons
document.addEventListener('click', function (e) {
    var target = e.target;
    if (
        (target.tagName === 'A' || target.tagName === 'BUTTON' || target.type === 'submit') &&
        target.getAttribute('data-bs-toggle') !== 'dropdown' && target.getAttribute('target') !== '_blank' &&
        target.getAttribute('data-bs-toggle') !== 'tooltip' && target.getAttribute('href') !== '#' &&
        target.getAttribute('data-popup') !== 'yes'
    ) {
        preloaderTimeout = setTimeout(showPreloader, 500);
    }
});
