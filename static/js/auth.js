$(document).ready(function () {
    // 1. Flip Animation
    $('#toSignup').click(function (e) {
        e.preventDefault();
        $('#flipper').addClass('flipped');
    });

    $('#toLogin').click(function (e) {
        e.preventDefault();
        $('#flipper').removeClass('flipped');
    });
});
