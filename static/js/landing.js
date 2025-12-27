$(document).ready(function () {

    // ==========================================
    // 1. AUTHENTICATION: FLIP CARD LOGIC
    // ==========================================

    // Switch to Signup (Flip to Back)
    $('#toSignup').on('click', function (e) {
        e.preventDefault();
        $('#flipper').addClass('flipped');
    });

    // Switch to Login (Flip to Front)
    $('#toLogin').on('click', function (e) {
        e.preventDefault();
        $('#flipper').removeClass('flipped');
    });


    // ==========================================
    // 2. FORM SUBMISSION (SIMULATED AUTH)
    // ==========================================

    $('#loginForm, #signupForm').on('submit', function (e) {
        e.preventDefault();
        const $btn = $(this).find('button');
        const originalText = $btn.html();

        // Add loading state to button
        $btn.prop('disabled', true)
            .html('<i class="fas fa-circle-notch fa-spin me-2"></i> Verifying...');

        // Simulate a database check/network delay
        setTimeout(() => {
            // Success animation
            $btn.removeClass('btn-primary-grad').addClass('btn-success')
                .html('<i class="fas fa-check me-2"></i> Access Granted');

            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 800);

        }, 1500);
    });


    // ==========================================
    // 3. DASHBOARD: SEARCH & FILTERING
    // ==========================================

    $('#dbSearch').on('keyup', function () {
        const value = $(this).val().toLowerCase();

        // Filter rows in the asset table
        $("#assetTable tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });


    // ==========================================
    // 4. DASHBOARD: ANALYTICS CHART (Chart.js)
    // ==========================================

    // Only run if the chart canvas exists on the current page
    const chartCanvas = document.getElementById('maintenanceChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');

        // Create a beautiful gradient for the line chart
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.4)');
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Resolved Requests',
                    data: [18, 12, 28, 22, 34, 42, 38],
                    borderColor: '#6366f1',
                    borderWidth: 3,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#6366f1',
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

});