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

    // 2. Simulated Login/Signup redirect
    $('#loginForm, #signupForm').submit(function (e) {
        e.preventDefault();
        const btn = $(this).find('button');
        const originalText = btn.text();

        // Show loading state
        btn.prop('disabled', true).html('<i class="fas fa-circle-notch fa-spin"></i> Processing...');

        setTimeout(() => {
            // Redirect to dashboard (create dashboard.html)
            window.location.href = 'dashboard.html';
        }, 1500);
    });

    // 3. Simple Search Filter (for Dashboard)
    $('#dbSearch').on('keyup', function () {
        var value = $(this).val().toLowerCase();
        $("#assetTable tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});