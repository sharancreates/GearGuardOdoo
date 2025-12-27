document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.task-card[draggable="true"]');
    const columns = document.querySelectorAll('.kanban-col');

    let draggedCard = null;

    cards.forEach(card => {
        card.addEventListener('dragstart', (e) => {
            draggedCard = card;
            e.dataTransfer.setData('text/plain', card.dataset.id);
            setTimeout(() => card.classList.add('dragging'), 0);
        });

        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
            draggedCard = null;
            columns.forEach(col => col.classList.remove('drag-over'));
        });
    });

    columns.forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            column.classList.add('drag-over');
        });

        column.addEventListener('dragleave', () => {
            column.classList.remove('drag-over');
        });

        column.addEventListener('drop', (e) => {
            e.preventDefault();
            column.classList.remove('drag-over');

            if (!draggedCard) return;

            const newStage = column.dataset.stage;
            const oldStage = draggedCard.closest('.kanban-col').dataset.stage;

            if (!isValidMove(oldStage, newStage)) {
                alert(`Cannot move from ${oldStage} to ${newStage}`);
                return;
            }

            column.appendChild(draggedCard);
            updateStageOnServer(draggedCard.dataset.id, newStage);
        });
    });
});

function isValidMove(fromStage, toStage) {
    const rules = {
        "New": ["In Progress"],
        "In Progress": ["Repaired", "Scrap"],
        "Repaired": [],
        "Scrap": []
    };
    return rules[fromStage]?.includes(toStage);
}

function updateStageOnServer(requestId, newStage) {
    fetch('/maintenance/api/update_stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            request_id: requestId,
            new_stage: newStage
        })
    }).then(res => {
        if (!res.ok) {
            alert("Failed to update request stage");
        }
    });
}
