document.addEventListener("DOMContentLoaded", () => {
    const stateDisplay = document.getElementById("state-display");
    const volumeSlider = document.getElementById("volume");
    const fileList = document.getElementById("file-list");
    const audioPlayer = document.getElementById("audio-player");
    let currentFile = null;

    const toggleButtons = document.querySelectorAll(".toggle-btn");
    const testBtn = document.getElementById("test-sound-btn");

    if (testBtn) {
        testBtn.addEventListener("click", () => {
            fetch('/api/midi', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ msg: 'BXon' })
                }).then(res => {
                    if (!res.ok) console.error('MIDI error', res.status);
                });
        });
    }

    function updateButton(btn, isOn) {
        const name = btn.dataset.device.replace(/_/g, ' ');
        btn.textContent = `${name}: ${isOn ? 'Вкл' : 'Выкл'}`;
        btn.dataset.state = isOn ? 'on' : 'off';
        btn.style.backgroundColor = isOn ? '#4cd137' : '#e84118';
    }

    toggleButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const currentState = btn.dataset.state === 'on';
            const cmd = currentState ? `${btn.dataset.device}Off` : `${btn.dataset.device}On`;
            fetch("/api/command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ cmd })
            }).then(res => {
                if (!res.ok) alert("Ошибка отправки команды");
                else updateButton(btn, !currentState);
            });
        });
    });

    // --- SSE: обновление состояния МК ---
    if (!!window.EventSource) {
        const evtSource = new EventSource("/api/subscribe");
        evtSource.onmessage = (e) => {
            console.log("Состояние МК:", e.data); // выводим в консоль для отладки

            try {
                const state = JSON.parse(e.data);

                // Обновляем toggle-кнопки
                toggleButtons.forEach(btn => {
                    if (state[btn.dataset.device] !== undefined) {
                        updateButton(btn, state[btn.dataset.device]);
                    }
                });

                // Обновляем блок состояния визуально
                stateDisplay.innerHTML = ""; // очистка
                const stateElements = [
                    "Свет на картину","Кнопка_в_полу_1", "Кнопка_в_полу_2", "Кнопка_в_полу_3",
                    "Светильник_1", "Светильник_2", "Светильник_3",
                    "Светильник_4", "Светильник_5", "Светильник_6",
                    "Символ_1", "Символ_2", "Символ_3",
                    "Символ_4", "Символ_5", "Символ_6",
                    "Статуетка_1", "Статуетка_2", "Статуетка_3"
                ];

                stateElements.forEach(key => {
                    if (state[key] !== undefined) {
                        const div = document.createElement("div");
                        div.className = "state-item " + (state[key] ? "state-on" : "state-off");
                        div.textContent = key.replace(/_/g, ' ');
                        stateDisplay.appendChild(div);
                    }
                });
            } catch(err) {
                // Игнорируем если не JSON
            }
        };
    }

    // --- Список аудиофайлов ---
    fetch("/api/files")
        .then(res => res.json())
        .then(files => {
            fileList.innerHTML = "";
            files.forEach(f => {
                const li = document.createElement("li");
                li.textContent = f;
                li.addEventListener("click", () => {
                    currentFile = f;
                    audioPlayer.src = `/static/media/${f}`;
                    audioPlayer.style.display = "block";
                    audioPlayer.play();
                });
                fileList.appendChild(li);
            });
        });

    // --- Управление аудио ---
    volumeSlider.addEventListener("input", () => {
        audioPlayer.volume = volumeSlider.value / 100;
    });

    document.getElementById("play-btn").addEventListener("click", () => {
        if (currentFile) audioPlayer.play();
    });
    document.getElementById("pause-btn").addEventListener("click", () => audioPlayer.pause());
    document.getElementById("stop-btn").addEventListener("click", () => {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
    });
});
