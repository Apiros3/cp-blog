
function init() {
    document.querySelectorAll('a').forEach((el) => {
        el.setAttribute('rel', 'noopener noreferrer');
        el.setAttribute('target', '_blank');
    });
}
