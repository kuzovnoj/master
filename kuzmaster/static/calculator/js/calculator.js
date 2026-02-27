document.addEventListener('DOMContentLoaded', function() {
    // Получаем все канвасы
    const canvases = document.querySelectorAll('.overlay-canvas');
    
    // Хранилище для контуров деталей
    const partsByProjection = {};
    
    // Загружаем данные о деталях
    const partsData = JSON.parse(document.getElementById('parts-data').textContent);
    window.partsData = partsData; // Делаем глобальными
    
    // Группируем детали по проекциям
    partsData.forEach(part => {
        if (!partsByProjection[part.projection_id]) {
            partsByProjection[part.projection_id] = [];
        }
        partsByProjection[part.projection_id].push(part);
    });
    
    // Функция для получения ID выбранных деталей
    function getSelectedPartIds() {
        const selectedIds = [];
        // Ищем все строки в таблице выбранных деталей
        const selectedRows = document.querySelectorAll('.selected-parts-table tbody tr');
        
        selectedRows.forEach(row => {
            // Получаем название детали из первой ячейки
            const partNameCell = row.querySelector('td:first-child');
            if (partNameCell) {
                const partName = partNameCell.textContent.trim();
                // Ищем деталь по имени в partsData
                const foundPart = partsData.find(p => p.name === partName);
                if (foundPart) {
                    selectedIds.push(foundPart.id);
                }
            }
        });
        
        return selectedIds;
    }
    
    // Функция для получения ID выбранных деталей и их услуг
    function getSelectedPartsWithServices() {
        const selectedParts = [];
        const selectedRows = document.querySelectorAll('.selected-parts-table tbody tr');
        
        selectedRows.forEach(row => {
            const partNameCell = row.querySelector('td:first-child');
            const serviceCell = row.querySelector('td:nth-child(2) select');
            
            if (partNameCell && serviceCell) {
                const partName = partNameCell.textContent.trim();
                const serviceId = serviceCell.value;
                const serviceName = serviceCell.options[serviceCell.selectedIndex].text;
                
                // Ищем деталь по имени
                const foundPart = partsData.find(p => p.name === partName);
                if (foundPart) {
                    // Ищем услугу у этой детали
                    const service = foundPart.services.find(s => s.id == serviceId);
                    if (service) {
                        selectedParts.push({
                            partId: foundPart.id,
                            serviceId: service.id,
                            serviceName: service.name,
                            color: service.color || 'rgba(40, 167, 69, 0.2)' // Цвет по умолчанию
                        });
                    }
                }
            }
        });
        
        return selectedParts;
    }

    // Функция для перерисовки всех канвасов
    function redrawAllCanvases() {
        const selectedParts = getSelectedPartsWithServices();
        console.log('Перерисовка канвасов, выбранные детали:', selectedParts);
        
        canvases.forEach(canvas => {
            const ctx = canvas.getContext('2d');
            const projectionId = canvas.dataset.projectionId;
            const parts = partsByProjection[projectionId] || [];
            
            // Очищаем канвас
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Рисуем выбранные детали
            parts.forEach(part => {
                // Создаем путь если его нет
                if (!part.path) {
                    try {
                        part.path = new Path2D(part.coordinates);
                    } catch (e) {
                        console.error('Ошибка при создании Path2D для детали', part.name, e);
                        return;
                    }
                }
                
                // Ищем, выбрана ли эта деталь
                const selectedPart = selectedParts.find(sp => sp.partId === part.id);
                
                if (selectedPart) {
                    // Используем цвет из услуги
                    ctx.fillStyle = selectedPart.color;
                    ctx.fill(part.path);
                    
                    // Темный контур для выделения
                    ctx.strokeStyle = '#333';
                    ctx.lineWidth = 1.5;
                    ctx.stroke(part.path);
                }
            });
        });
    }

    function handleMouseMove(e) {
        const canvas = e.currentTarget;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const parts = canvas.parts || [];
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        // Получаем выбранные детали
        const selectedParts = getSelectedPartsWithServices();
        
        // Очищаем канвас
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Сначала рисуем все выбранные детали с их цветами
        parts.forEach(part => {
            if (!part.path) return;
            
            const selectedPart = selectedParts.find(sp => sp.partId === part.id);
            
            if (selectedPart) {
                ctx.fillStyle = selectedPart.color;
                ctx.fill(part.path);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 1.5;
                ctx.stroke(part.path);
            }
        });
        
        // Затем проверяем наведение
        let found = false;
        parts.forEach(part => {
            if (part.path && ctx.isPointInPath(part.path, x, y)) {
                const selectedPart = selectedParts.find(sp => sp.partId === part.id);
                
                if (selectedPart) {
                    // Если деталь уже выбрана - усиливаем её цвет при наведении
                    ctx.fillStyle = adjustColor(selectedPart.color, 1.2); // Ярче на 20%
                    ctx.fill(part.path);
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 2.5;
                    ctx.stroke(part.path);
                } else {
                    // Если деталь не выбрана - показываем полупрозрачный серый
                    ctx.fillStyle = 'rgba(128, 128, 128, 0.3)';
                    ctx.fill(part.path);
                    ctx.strokeStyle = '#666';
                    ctx.lineWidth = 2;
                    ctx.stroke(part.path);
                }
                
                found = true;
            }
        });
        
        canvas.style.cursor = found ? 'pointer' : 'default';
    }

    // Вспомогательная функция для изменения яркости цвета
    function adjustColor(color, factor) {
        if (color.startsWith('rgba')) {
            // Парсим rgba
            const matches = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+),?\s*([\d.]+)?\)/);
            if (matches) {
                const r = Math.min(255, Math.round(matches[1] * factor));
                const g = Math.min(255, Math.round(matches[2] * factor));
                const b = Math.min(255, Math.round(matches[3] * factor));
                const a = matches[4] || 0.3;
                return `rgba(${r}, ${g}, ${b}, ${a})`;
            }
        }
        return color;
    }
    
    // Наблюдатель за изменениями в DOM (для отслеживания добавления/удаления деталей)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Если изменилась таблица с деталями - перерисовываем
                if (mutation.target.closest('.selected-parts-table')) {
                    redrawAllCanvases();
                }
            }
        });
    });
    
    // Начинаем наблюдение за таблицей
    const tableContainer = document.querySelector('.selected-parts-section');
    if (tableContainer) {
        observer.observe(tableContainer, { childList: true, subtree: true });
    }
    
    // Настраиваем каждый канвас
    canvases.forEach(canvas => {
        const projectionId = canvas.dataset.projectionId;
        const parts = partsByProjection[projectionId] || [];
        
        // Сохраняем части на канвасе для обработчиков
        canvas.parts = parts;
        
        // Добавляем обработчики событий
        canvas.addEventListener('mousemove', handleMouseMove);
        canvas.addEventListener('mouseleave', handleMouseLeave);
        canvas.addEventListener('click', handleClick);
    });
    
    // Первоначальная отрисовка
    redrawAllCanvases();
    
    
    function handleMouseLeave(e) {
        const canvas = e.currentTarget;
        if (!canvas) return;
        // Просто перерисовываем канвас в нормальное состояние
        redrawAllCanvases();
        canvas.style.cursor = 'default';
    }
    
    function handleClick(e) {
        console.log('handleClick вызван');
        
        const canvas = e.currentTarget;  // Получаем canvas из события
        if (!canvas) {
            console.error('Canvas не найден');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.error('Не удалось получить контекст canvas');
            return;
        }
        
        const parts = canvas.parts || [];  // Получаем parts из canvas
        const rect = canvas.getBoundingClientRect();
        
        // Защита от деления на ноль
        if (rect.width === 0 || rect.height === 0) {
            console.error('Canvas имеет нулевой размер');
            return;
        }
        
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        console.log(`Координаты клика: x=${x}, y=${y}, деталей: ${parts.length}`);
        
        // Ищем деталь, на которую кликнули
        let found = false;
        for (let part of parts) {
            if (part.path) {
                try {
                    if (ctx.isPointInPath(part.path, x, y)) {
                        console.log('Клик на деталь:', part.name);
                        if (typeof window.showServiceModal === 'function') {
                            window.showServiceModal(part);
                            found = true;
                            break;
                        } else {
                            console.error('showServiceModal не определена');
                        }
                    }
                } catch (err) {
                    console.error('Ошибка при проверке точки в пути:', err, part);
                }
            }
        }
        
        if (!found) {
            console.log('Клик не попал ни в одну деталь');
        }
    }
    
    function showServiceModal(part) {
        console.log('🟢 showServiceModal вызвана для детали:', part);

        // --- КРИТИЧЕСКАЯ ПРОВЕРКА: есть ли услуги у детали? ---
        let servicesToShow = part.services;
        
        // Если услуги не пришли или это пустой массив
        if (!servicesToShow || servicesToShow.length === 0) {
            console.error('🔴 ОШИБКА: У детали "' + part.name + '" нет массива услуг (services)!');
            console.log('Пробуем найти услуги в глобальном partsData...');

            // Запасной вариант: попробовать найти деталь в глобальных данных и взять услуги оттуда
            if (window.partsData) {
                const originalPart = window.partsData.find(p => p.id === part.id);
                if (originalPart && originalPart.services && originalPart.services.length > 0) {
                    console.log('🟢 Услуги найдены в глобальных данных!', originalPart.services);
                    servicesToShow = originalPart.services;
                } else {
                    console.error('🔴 Услуги не найдены даже в глобальных данных.');
                    alert(`Для детали "${part.name}" не настроены услуги в админке.`);
                    return; // Выходим, не показываем пустое окно
                }
            } else {
                alert(`Ошибка загрузки данных. Попробуйте обновить страницу.`);
                return;
            }
        }

        console.log('Выбрана деталь:', part);
        console.log('Доступные услуги:', servicesToShow);
        
        // Получаем CSRF-токен
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        const csrftoken = getCookie('csrftoken');

        // Удаляем предыдущие модальные окна
        document.querySelectorAll('.modal').forEach(m => m.remove());

        // Создаем HTML-код для каждой услуги с цветным превью
        const serviceOptionsHtml = servicesToShow.map(service => `
            <label class="service-option">
                <input type="radio" name="service_id" value="${service.id}" required>
                <span class="service-color-preview" style="background-color: ${service.color}; width: 30px; height: 20px; display: inline-block; border-radius: 4px; margin-right: 10px;"></span>
                <span class="service-name">${service.name}</span>
                <span class="service-price">${service.price} ₽</span>
            </label>
        `).join('');

        // Создаем модальное окно
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Выберите услугу для детали "${part.name}"</h3>
                <form method="post" action="/calculator/part/add/">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                    <input type="hidden" name="part_id" value="${part.id}">
                    <div class="service-options">
                        ${serviceOptionsHtml}
                    </div>
                    <div class="modal-actions">
                        <button type="submit" class="btn-primary">Добавить</button>
                        <button type="button" class="btn-secondary" onclick="this.closest('.modal').remove()">Отмена</button>
                    </div>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        console.log('🟢 Модальное окно с услугами добавлено в DOM');
    }
    
    // Вспомогательная функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Глобальные функции для модальных окон
window.showAppointmentModal = function() {
    console.log('Открытие модального окна записи');
    document.getElementById('appointmentModal').style.display = 'flex';
};

window.showCallbackModal = function() {
    console.log('Открытие модального окна звонка');
    document.getElementById('callbackModal').style.display = 'flex';
};

window.closeModal = function(modalId) {
    console.log('Закрытие модального окна:', modalId);
    document.getElementById(modalId).style.display = 'none';
};

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Обработка отправки формы записи
document.addEventListener('DOMContentLoaded', function() {
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Отправка формы записи');
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/calculator/api/create-appointment/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                console.log('Ответ сервера:', data);
                
                if (data.success) {
                    alert('✓ ' + data.message);
                    window.closeModal('appointmentModal');
                    this.reset();
                } else {
                    if (data.errors) {
                        const errorMessages = Object.values(data.errors).flat().join('\n');
                        alert('Ошибка:\n' + errorMessages);
                    } else {
                        alert('Ошибка при отправке формы');
                    }
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отправке. Попробуйте позже.');
            }
        });
    }

    const callbackForm = document.getElementById('callbackForm');
    if (callbackForm) {
        callbackForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Отправка формы звонка');
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/calculator/api/create-callback/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                console.log('Ответ сервера:', data);
                
                if (data.success) {
                    alert('✓ ' + data.message);
                    window.closeModal('callbackModal');
                    this.reset();
                } else {
                    if (data.errors) {
                        const errorMessages = Object.values(data.errors).flat().join('\n');
                        alert('Ошибка:\n' + errorMessages);
                    } else {
                        alert('Ошибка при отправке формы');
                    }
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отправке. Попробуйте позже.');
            }
        });
    }
});

// ========== ГЛОБАЛЬНЫЕ ФУНКЦИИ ==========
// Делаем showServiceModal доступной глобально
window.showServiceModal = function(part) {
    console.log('🟢 [GLOBAL] showServiceModal вызвана для детали:', part);
    
    // Проверяем, что услуги есть
    let servicesToShow = part.services;
    
    if (!servicesToShow || servicesToShow.length === 0) {
        console.error('❌ У детали нет услуг');
        alert('Для этой детали временно нет доступных услуг');
        return;
    }
    
    // Получаем CSRF токен
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
                }
            }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    // Удаляем предыдущие модальные окна
    document.querySelectorAll('.modal').forEach(m => m.remove());
    
    // Создаем HTML для услуг
    const serviceOptionsHtml = servicesToShow.map(service => `
        <label class="service-option" style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0; padding: 10px; background: #363636; border: 1px solid #4a4a4a; border-radius: 5px; cursor: pointer;">
            <span style="display: flex; align-items: center;">
                <input type="radio" name="service_id" value="${service.id}" required style="margin-right: 10px;">
                <span style="color: #e0e0e0;">${service.name}</span>
            </span>
            <span style="color: #67b26f; font-weight: bold;">${service.price} ₽</span>
        </label>
    `).join('');
    
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); display: flex; justify-content: center; align-items: center; z-index: 10000;';
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = 'background: #2d2d2d; padding: 30px; border-radius: 15px; max-width: 500px; width: 90%; border: 1px solid #4a4a4a;';
    
    modalContent.innerHTML = `
        <h3 style="color: #e0e0e0; margin-bottom: 20px; font-family: Montserrat, sans-serif;">Выберите услугу для детали "${part.name}"</h3>
        <form id="service-form-${part.id}" method="post" action="/calculator/part/add/">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
            <input type="hidden" name="part_id" value="${part.id}">
            <div style="margin-bottom: 20px; max-height: 400px; overflow-y: auto;">
                ${serviceOptionsHtml}
            </div>
            <div style="display: flex; gap: 10px; justify-content: flex-end;">
                <button type="button" onclick="this.closest('.modal').remove()" style="background: #404040; color: white; border: 1px solid #4a4a4a; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px;">Отмена</button>
                <button type="submit" style="background: linear-gradient(135deg, #4a90e2, #67b26f); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px;">Добавить</button>
            </div>
        </form>
    `;
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    console.log('✅ Модальное окно добавлено в DOM');
    
    // Добавляем обработчик отправки формы
    document.getElementById(`service-form-${part.id}`).addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/calculator/part/add/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
            
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Ошибка: ' + JSON.stringify(data.errors));
                }
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке');
        }
    });
};

// Делаем вспомогательные функции глобальными
window.showAppointmentModal = function() {
    console.log('Открытие модального окна записи');
    const modal = document.getElementById('appointmentModal');
    if (modal) modal.style.display = 'flex';
};

window.showCallbackModal = function() {
    console.log('Открытие модального окна звонка');
    const modal = document.getElementById('callbackModal');
    if (modal) modal.style.display = 'flex';
};

window.closeModal = function(modalId) {
    console.log('Закрытие модального окна:', modalId);
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
};

// Проверяем, что всё определилось
console.log('✅ Глобальные функции загружены:', {
    showServiceModal: typeof window.showServiceModal === 'function',
    showAppointmentModal: typeof window.showAppointmentModal === 'function',
    showCallbackModal: typeof window.showCallbackModal === 'function'
});