// Workout Timer / Chronomètre
class WorkoutTimer {
    constructor() {
        this.seconds = 0;
        this.interval = null;
        this.isRunning = false;
        this.isPaused = false;
    }

    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.isPaused = false;
            this.interval = setInterval(() => {
                this.seconds++;
                this.updateDisplay();
            }, 1000);
        }
    }

    pause() {
        if (this.isRunning && !this.isPaused) {
            this.isPaused = true;
            clearInterval(this.interval);
        }
    }

    resume() {
        if (this.isPaused) {
            this.start();
        }
    }

    stop() {
        this.isRunning = false;
        this.isPaused = false;
        clearInterval(this.interval);
        this.seconds = 0;
        this.updateDisplay();
    }

    reset() {
        this.stop();
    }

    updateDisplay() {
        const hours = Math.floor(this.seconds / 3600);
        const minutes = Math.floor((this.seconds % 3600) / 60);
        const secs = this.seconds % 60;

        const display = `${this.pad(hours)}:${this.pad(minutes)}:${this.pad(secs)}`;

        const timerDisplay = document.getElementById('timer-display');
        if (timerDisplay) {
            timerDisplay.textContent = display;
        }

        // Save to localStorage
        localStorage.setItem('workout_timer', this.seconds);
    }

    pad(num) {
        return num.toString().padStart(2, '0');
    }

    loadFromStorage() {
        const saved = localStorage.getItem('workout_timer');
        if (saved) {
            this.seconds = parseInt(saved);
            this.updateDisplay();
        }
    }
}

// Initialize timer on page load
let workoutTimer;

document.addEventListener('DOMContentLoaded', () => {
    const timerContainer = document.getElementById('timer-container');

    if (timerContainer) {
        workoutTimer = new WorkoutTimer();
        workoutTimer.loadFromStorage();

        // Button event listeners
        document.getElementById('timer-start')?.addEventListener('click', () => {
            workoutTimer.start();
            updateTimerButtons();
        });

        document.getElementById('timer-pause')?.addEventListener('click', () => {
            workoutTimer.pause();
            updateTimerButtons();
        });

        document.getElementById('timer-resume')?.addEventListener('click', () => {
            workoutTimer.resume();
            updateTimerButtons();
        });

        document.getElementById('timer-stop')?.addEventListener('click', () => {
            workoutTimer.stop();
            updateTimerButtons();
        });
    }
});

function updateTimerButtons() {
    const startBtn = document.getElementById('timer-start');
    const pauseBtn = document.getElementById('timer-pause');
    const resumeBtn = document.getElementById('timer-resume');
    const stopBtn = document.getElementById('timer-stop');

    if (workoutTimer.isRunning && !workoutTimer.isPaused) {
        startBtn?.classList.add('d-none');
        pauseBtn?.classList.remove('d-none');
        resumeBtn?.classList.add('d-none');
        stopBtn?.classList.remove('d-none');
    } else if (workoutTimer.isPaused) {
        startBtn?.classList.add('d-none');
        pauseBtn?.classList.add('d-none');
        resumeBtn?.classList.remove('d-none');
        stopBtn?.classList.remove('d-none');
    } else {
        startBtn?.classList.remove('d-none');
        pauseBtn?.classList.add('d-none');
        resumeBtn?.classList.add('d-none');
        stopBtn?.classList.add('d-none');
    }
}
