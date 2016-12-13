/**
 * Created by renefernandez on 28/09/16.
 */
$('.message .close')
    .on('click', function () {
        $(this)
            .closest('.message')
            .transition('fade');
    });

$("a.sidebar-toggle").click(function () {
    $('.ui.sidebar').sidebar('toggle');
});