// script.js

document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.card-clickable');

    cards.forEach((card) => {
        card.addEventListener('click', () => {
            card.classList.toggle('card-clicked');
            const cardFooter = card.querySelector('.card-footer');
            cardFooter.style.display = cardFooter.style.display === 'none' ? 'block' : 'none';
        });
    });
});
