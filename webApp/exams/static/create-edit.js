const htmlElement = document.documentElement;
const toggleButton = document.getElementById('toggleMode');

toggleButton.addEventListener('click', () => {
    if (htmlElement.classList.contains('light')) {
        htmlElement.classList.remove('light');
        htmlElement.classList.add('dark');
    } else {
        htmlElement.classList.remove('dark');
        htmlElement.classList.add('light');
    }
});