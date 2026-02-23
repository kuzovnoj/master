document.addEventListener('DOMContentLoaded', function() {
    // Получаем все канвасы
    const canvases = document.querySelectorAll('.overlay-canvas');
    
    // Хранилище для контуров деталей
    const partsByProjection = {};
    
    // Загружаем данные о деталях
    const partsData = JSON.parse(document.getElementById('parts-data').textContent);
    
    // Группируем детали по проекциям
    partsData.forEach(part => {
        if (!partsByProjection[part.projection_id]) {
            partsByProjection[part.projection_id] = [];
        }
        partsByProjection[part.projection_id].push(part);
    });
    
    // Настраиваем каждый канвас
    canvases.forEach(canvas => {
        const projectionId = canvas.dataset.projectionId;
        const ctx = canvas.getContext('2d');
        
        // Загружаем детали для этой проекции
        const parts = partsByProjection[projectionId] || [];
        
        // Рисуем контуры
        drawParts(ctx, parts, projectionId);
        
        // Добавляем обработчики событий
        canvas.addEventListener('mousemove', (e) => handleMouseMove(e, canvas, parts));
        canvas.addEventListener('mouseleave', () => handleMouseLeave(canvas, parts));
        canvas.addEventListener('click', (e) => handleClick(e, canvas, parts));
    });
    
    function drawParts(ctx, parts, projectionId) {
        // Очищаем канвас
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        
        // Рисуем каждую деталь
        parts.forEach(part => {
            // Парсим координаты (ожидаем SVG path)
            const path = new Path2D(part.coordinates);
            
            // Сохраняем путь для детали
            part.path = path;
            
            // Рисуем контур
            ctx.strokeStyle = '#007bff';
            ctx.lineWidth = 2;
            ctx.stroke(path);
        });
    }
    
    function handleMouseMove(e, canvas, parts) {
        const ctx = canvas.getContext('2d');
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        // Получаем координаты мыши относительно канваса
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        // Перерисовываем все контуры (сбрасываем подсветку)
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Проверяем каждую деталь
        let found = false;
        parts.forEach(part => {
            if (part.path) {
                if (ctx.isPointInPath(part.path, x, y)) {
                    // Подсвечиваем деталь
                    ctx.strokeStyle = '#ff0000';
                    ctx.lineWidth = 3;
                    ctx.stroke(part.path);
                    
                    // Добавляем полупрозрачную заливку
                    ctx.fillStyle = 'rgba(255, 0, 0, 0.1)';
                    ctx.fill(part.path);
                    
                    found = true;
                } else {
                    // Обычный контур
                    ctx.strokeStyle = '#007bff';
                    ctx.lineWidth = 2;
                    ctx.stroke(part.path);
                }
            }
        });
        
        // Меняем курсор
        canvas.style.cursor = found ? 'pointer' : 'default';
    }
    
    function handleMouseLeave(canvas, parts) {
        const ctx = canvas.getContext('2d');
        
        // Сбрасываем подсветку
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        parts.forEach(part => {
            if (part.path) {
                ctx.strokeStyle = '#007bff';
                ctx.lineWidth = 2;
                ctx.stroke(part.path);
            }
        });
        
        canvas.style.cursor = 'default';
    }
    
    function handleClick(e, canvas, parts) {
        const ctx = canvas.getContext('2d');
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        // Ищем деталь, на которую кликнули
        for (let part of parts) {
            if (part.path && ctx.isPointInPath(part.path, x, y)) {
                // Показываем модальное окно с выбором услуги
                showServiceModal(part);
                break;
            }
        }
    }
    
    function showServiceModal(part) {
        // Получаем список услуг из данных
        let services = [];
        const servicesElement = document.getElementById('services-data');
        if (servicesElement) {
            try {
                services = JSON.parse(servicesElement.textContent);
                console.log('Услуги загружены:', services);
            } catch (e) {
                console.error('Ошибка парсинга услуг:', e);
            }
        }
        
        // Если не получилось, используем запасной вариант
        if (services.length === 0) {
            services = [
                {id: 1, name: 'Полировка'},
                {id: 2, name: 'Покраска'},
                {id: 3, name: 'Ремонт'}
            ];
        }
        
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
                        ${services.map(service => `
                            <label class="service-option">
                                <input type="radio" name="service_id" value="${service.id}" required>
                                ${service.name}
                            </label>
                        `).join('')}
                    </div>
                    <div class="modal-actions">
                        <button type="submit" class="btn-primary">Добавить</button>
                        <button type="button" class="btn-secondary" onclick="this.closest('.modal').remove()">Отмена</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
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