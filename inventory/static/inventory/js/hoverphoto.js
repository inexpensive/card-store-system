var cardFigure = document.getElementsByClassName('card-picture')
window.onmousemove = function (e) {
    var x = e.clientX,
        y = e.clientY;
    for (var i = 0; i < cardFigure.length; i++) {
        cardFigure[i].style.top = (y + 20) + 'px';
        cardFigure[i].style.left = (x + 20) + 'px';
    }
};