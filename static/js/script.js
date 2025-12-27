$(document).ready(function () {
    // Sample Data Array
    const maintenanceData = [
        { subject: "AC Unit Leakage", employee: "Mitchell Admin", technician: "Aka Foster", category: "HVAC", stage: "New Request", company: "My Company" },
        { subject: "Brake Pad Replacement", employee: "Sarah Connor", technician: "John Doe", category: "Vehicle", stage: "In Progress", company: "Fleet Corp" },
        { subject: "Server Overheating", employee: "Kevin Flynn", technician: "Alan Bradley", category: "Computer", stage: "High Priority", company: "ENCOM" },
        { subject: "Hydraulic Press Noise", employee: "Ellen Ripley", technician: "Bishop", category: "Machine", stage: "Awaiting Parts", company: "Weyland-Yutani" }
    ];

    // Function to render table
    function renderTable(data) {
        const tableBody = $('#requestsTable tbody');
        tableBody.empty();

        data.forEach(item => {
            const row = `
                <tr>
                    <td><strong>${item.subject}</strong></td>
                    <td>${item.employee}</td>
                    <td>${item.technician}</td>
                    <td><span class="cat-tag">${item.category}</span></td>
                    <td><span class="badge ${getStageClass(item.stage)}">${item.stage}</span></td>
                    <td>${item.company}</td>
                </tr>
            `;
            tableBody.append(row);
        });
    }

    // Helper for Badge Colors
    function getStageClass(stage) {
        switch (stage) {
            case 'New Request': return 'bg-primary';
            case 'In Progress': return 'bg-warning text-dark';
            case 'High Priority': return 'bg-danger';
            default: return 'bg-secondary';
        }
    }

    // Initial Render
    renderTable(maintenanceData);

    // Filter Logic
    $('#dashboardSearch').on('keyup', function () {
        const value = $(this).val().toLowerCase();
        const filtered = maintenanceData.filter(item =>
            item.subject.toLowerCase().includes(value) ||
            item.technician.toLowerCase().includes(value) ||
            item.category.toLowerCase().includes(value)
        );
        renderTable(filtered);
    });

    // Button Animation
    $('#newRequestBtn').click(function () {
        $(this).html('<i class="fas fa-spinner fa-spin me-2"></i>Opening...');
        setTimeout(() => {
            alert("This would open the 'Add Asset' form!");
            $(this).html('<i class="fas fa-plus me-2"></i>New Request');
        }, 800);
    });
});