// Generate 30 days dynamically
const calendarDays = document.getElementById('calendarDays');
for (let i = 1; i <= 30; i++) {
    const dayCell = document.createElement('div');
    dayCell.className = 'day-cell';
    dayCell.innerHTML = `<div class="day-num">${i}</div>`;
    calendarDays.appendChild(dayCell);
}

// Modal functionality
let selectedCell = null;

document.querySelectorAll('.day-cell').forEach(cell => {
    cell.addEventListener('click', () => {
        selectedCell = cell;
        const day = cell.querySelector('.day-num').innerText;
        document.getElementById('selectedDate').innerText = `Day ${day}`;
        document.getElementById('maintenanceModal').classList.remove('hidden');
    });
});

// Close modal
document.getElementById('closeModal').onclick = () => {
    document.getElementById('maintenanceModal').classList.add('hidden');
};

// Save task
document.getElementById('saveTask').onclick = () => {
    const name = document.getElementById('taskName').value;
    const priority = document.getElementById('priority').value;

    if (!name) return alert("Enter task name");

    const task = document.createElement('div');
    task.className = `task-tag ${priority}`;
    task.innerText = name;

    selectedCell.appendChild(task);
    document.getElementById('taskName').value = '';
    document.getElementById('maintenanceModal').classList.add('hidden');
};
