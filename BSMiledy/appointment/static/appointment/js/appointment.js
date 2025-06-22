document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.appointment-container');
    const masterSelect = document.getElementById('id_master');
    const dateInput = document.getElementById('id_date');
    const serviceDuration = container.dataset.serviceDuration;
    const slotsContainer = document.getElementById('available-slots');
    const timeInput = document.getElementById('id_time');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let selectedMaster = null;
    
    // Обработчик выбора мастера
    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            selectedMaster = this.value;
            slotsContainer.innerHTML = '';
            dateInput.disabled = !selectedMaster;
        });
    }
    
    // Обработчик выбора даты
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            if (!selectedMaster) return;
            
            const selectedDate = this.value;
            if (!selectedDate) return;
            
            fetchAvailableSlots(selectedMaster, selectedDate, serviceDuration);
        });
    }

    function fetchAvailableSlots(masterId, date, duration) {
        slotsContainer.innerHTML = '<p>Загрузка доступных слотов...</p>';
        
        fetch(`/appointment/available-slots/?master_id=${masterId}&date=${date}&duration=${duration}`, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сети');
            return response.json();
        })
        .then(data => {
            displayAvailableSlots(data.slots);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            slotsContainer.innerHTML = '<p class="error">Не удалось загрузить доступные слоты</p>';
        });
    }

    function displayAvailableSlots(slots) {
        slotsContainer.innerHTML = '';
        
        if (!slots || slots.length === 0) {
            slotsContainer.innerHTML = '<p>Нет доступных слотов для записи</p>';
            return;
        }
        
        const slotList = document.createElement('div');
        slotList.className = 'slot-list';
        
        slots.forEach(slot => {
            const slotElement = document.createElement('button');
            slotElement.type = 'button';
            slotElement.textContent = slot.time;
            slotElement.classList.add('time-slot');
            slotElement.dataset.time = slot.time;
            
            slotElement.addEventListener('click', function() {
                timeInput.value = this.dataset.time;
                document.querySelectorAll('.time-slot').forEach(el => {
                    el.classList.remove('selected');
                });
                this.classList.add('selected');
            });
            
            slotList.appendChild(slotElement);
        });
        
        slotsContainer.appendChild(slotList);
    }
});