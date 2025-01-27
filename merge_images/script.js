$(document).ready(function() {
    var d_canvas = document.getElementById('canvas');
    var context = d_canvas.getContext('2d');
    var background = document.getElementById('background');
    var balloon = document.getElementById('balloon');
    context.drawImage(background, 0, 0);

    $('#balloon').draggable();

    $('#draw').click(function() {
        var $balloon = $('#balloon'),
            $canvas = $('#canvas');
        var balloon_x = $balloon.offset().left - $canvas.offset().left,
            balloon_y = $balloon.offset().top - $canvas.offset().top;

        context.drawImage(balloon, balloon_x, balloon_y);

        $balloon.hide();
        $(this).attr('disabled', 'disabled');
    });
});