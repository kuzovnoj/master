document.addEventListener('DOMContentLoaded', function() {
    console.log('=== ДИАГНОСТИКА КАЛЬКУЛЯТОРА ===');
    
    // 1. Проверяем данные
    const partsDataElement = document.getElementById('parts-data');
    console.log('parts-data элемент найден:', !!partsDataElement);
    
    if (partsDataElement) {
        try {
            const partsData = JSON.parse(partsDataElement.textContent);
            console.log('Загружено деталей:', partsData.length);
            console.log('Детали:', partsData);
        } catch (e) {
            console.error('Ошибка парсинга parts-data:', e);
        }
    }
    
    // 2. Проверяем канвасы
    const canvases = document.querySelectorAll('.overlay-canvas');
    console.log('Найдено канвасов:', canvases.length);
    
    canvases.forEach((canvas, idx) => {
        console.log(`Канвас ${idx}:`, {
            id: canvas.id,
            width: canvas.width,
            height: canvas.height,
            visible: canvas.offsetParent !== null,
            position: window.getComputedStyle(canvas).position
        });
        
        // Временно закрасим канвас для проверки видимости
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        console.log('Канвас залит красным для проверки');
    });
    
    // 3. Проверяем изображения
    const images = document.querySelectorAll('.car-image');
    console.log('Найдено изображений:', images.length);
    images.forEach((img, idx) => {
        console.log(`Изображение ${idx}:`, {
            src: img.src,
            width: img.width,
            height: img.height,
            loaded: img.complete
        });
    });
    
    // 4. Проверяем контейнеры
    const containers = document.querySelectorAll('.image-container');
    console.log('Найдено контейнеров:', containers.length);
    containers.forEach((container, idx) => {
        console.log(`Контейнер ${idx}:`, {
            position: window.getComputedStyle(container).position,
            width: container.offsetWidth,
            height: container.offsetHeight
        });
    });
    
    // 5. Проверяем стили
    console.log('Проверка CSS:', {
        canvasDisplay: window.getComputedStyle(canvases[0]).display,
        canvasPosition: window.getComputedStyle(canvases[0]).position,
        canvasZIndex: window.getComputedStyle(canvases[0]).zIndex
    });
    
    alert('Диагностика завершена. Откройте консоль (F12) для просмотра результатов.');
});