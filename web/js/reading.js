var test = undefined;
var startSpeed = 300;
var endSpeed = 900;
var startPosition = 1000;
var fontSize = 50;

var text = "Немногим более 50 лет прошло с тех пор, как появилась первая электронная вычислительная машина. ";


var textObject = draw.plain(text).move(1000, '50%')
textObject.font({
    family: 'Georgia',
    size: fontSize,
    anchor: 'left',
    leading: 1,
});

var width = textObject.length();

var progress = function() {
    return Math.abs(textObject.x() - startPosition) / (width + startPosition);
}

var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
                          window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;


var move = function(delta) {
    var p = progress();
    var speed = startSpeed + p * (endSpeed - startSpeed);
    textObject.dx(-speed  * delta * 0.001);
    if(p > 1.0) {
        complete();
    }
};

var complete = function() {
    isAnimating = false;
    test.complete();
}

var isAnimating = false;
var lastFrame = 0;

var anim = function() {
    if(isAnimating) {
        var delta = Date.now() - lastFrame;
        move(delta);

    }
    requestAnimationFrame(anim);
    lastFrame = Date.now();
}
textObject.move(startPosition, '50%');

requestAnimationFrame(anim);

document.addEventListener('testInit', function(e) {
    console.log('testInit handler');
    test = e.detail.test;

    test.on('start', function(){
        isAnimating = true;
        console.log('reading started');
    });
});