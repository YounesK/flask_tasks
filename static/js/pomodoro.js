let duration = 25;
let timerInterval = null;

const durationElem = document.getElementById('duration');
const timerDisplay = document.getElementById('timer-display');
const minusBtn = document.getElementById('minus');
const plusBtn = document.getElementById('plus');
const startBtn = document.getElementById('start');
minusBtn.onclick = () => {
    if (duration > 1) {
        duration--;
        durationElem.textContent = duration;
    }
};

plusBtn.onclick = () => {
    duration++;
    durationElem.textContent = duration;
};

startBtn.onclick = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        timerDisplay.textContent = '';
        startBtn.textContent = 'Démarrer';
        return;
    }
    startBtn.textContent = 'Arrêter';
    startPomodoro(duration);
};

function startPomodoro(minutes) {
    let secondsLeft = minutes * 60;
    updateTimerDisplay(secondsLeft);

    timerInterval = setInterval(() => {
        secondsLeft--;
        updateTimerDisplay(secondsLeft);

        if (secondsLeft <= 0) {
            clearInterval(timerInterval);
            timerInterval = null;
            timerDisplay.textContent = 'Pomodoro terminé ! 🎉';
            startBtn.textContent = 'Démarrer';
            alert('Pomodoro terminé ! Pensez à marquer votre tâche comme terminée.');
        }
    }, 1000);
}

function updateTimerDisplay(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    timerDisplay.textContent = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
}

function toggleTask(taskId) {
    fetch(`/toggle/${taskId}`, { method: 'POST' })
        .then(() => location.reload())
        .catch(() => alert('Erreur lors de la mise à jour de la tâche.'));
}
