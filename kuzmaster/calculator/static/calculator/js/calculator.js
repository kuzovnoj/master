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
    
    // Функция для перерисовки всех канвасов
    function redrawAllCanvases() {
        const selectedPartIds = getSelectedPartIds();
        console.log('Перерисовка канвасов, выбранные детали:', selectedPartIds);
        
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
                
                // Если деталь выбрана - рисуем её
                if (selectedPartIds.includes(part.id)) {
                    // Зеленая заливка для выбранных деталей
                    ctx.fillStyle = 'rgba(40, 167, 69, 0.2)'; // Полупрозрачный зеленый
                    ctx.fill(part.path);
                    
                    // Зеленый контур
                    ctx.strokeStyle = '#28a745';
                    ctx.lineWidth = 2;
                    ctx.stroke(part.path);
                }
            });
        });
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
    
    function handleMouseMove(e) {
        const canvas = e.currentTarget;
        const ctx = canvas.getContext('2d');
        const parts = canvas.parts || [];
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        // Получаем выбранные детали
        const selectedPartIds = getSelectedPartIds();
        
        // Очищаем канвас
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Сначала рисуем все выбранные детали (зеленые)
        parts.forEach(part => {
            if (part.path && selectedPartIds.includes(part.id)) {
                ctx.fillStyle = 'rgba(40, 167, 69, 0.2)';
                ctx.fill(part.path);
                ctx.strokeStyle = '#28a745';
                ctx.lineWidth = 2;
                ctx.stroke(part.path);
            }
        });
        
        // Затем проверяем наведение
        let found = false;
        parts.forEach(part => {
            if (part.path && ctx.isPointInPath(part.path, x, y)) {
                // Подсвечиваем деталь (красным)
                ctx.strokeStyle = '#ff0000';
                ctx.lineWidth = 3;
                ctx.stroke(part.path);
                
                // Добавляем полупрозрачную красную заливку поверх зеленой
                ctx.fillStyle = 'rgba(255, 0, 0, 0.1)';
                ctx.fill(part.path);
                
                found = true;
            }
        });
        
        canvas.style.cursor = found ? 'pointer' : 'default';
    }
    
    function handleMouseLeave(e) {
        const canvas = e.currentTarget;
        // Просто перерисовываем канвас в нормальное состояние
        redrawAllCanvases();
        canvas.style.cursor = 'default';
    }
    
    function handleClick(e) {
        const canvas = e.currentTarget;
        const ctx = canvas.getContext('2d');
        const parts = canvas.parts || [];
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        // Ищем деталь, на которую кликнули
        for (let part of parts) {
            if (part.path && ctx.isPointInPath(part.path, x, y)) {
                showServiceModal(part);
                break;
            }
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

        // Создаем HTML-код для каждой услуги
        const serviceOptionsHtml = servicesToShow.map(service => `
            <label class="service-option">
                <input type="radio" name="service_id" value="${service.id}" required>
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