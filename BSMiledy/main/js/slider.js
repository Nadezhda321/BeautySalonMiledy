document.addEventListener('DOMContentLoaded', function() {
    const sliderWrapper = document.querySelector('.slider__wrapper');
    const slides = document.querySelectorAll('.slider__slide');
    const dots = document.querySelectorAll('.slider__dot');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    
    let currentSlide = 0;
    const slideCount = slides.length;
    
    // Инициализация слайдера
    function initSlider() {
        updateSlider();
        
        // Автоматическое перелистывание (опционально)
        setInterval(() => {
            nextSlide();
        }, 5000);
    }
    
    // Обновление слайдера
    function updateSlider() {
        sliderWrapper.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        // Обновление активной точки
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
    
    // Следующий слайд
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slideCount;
        updateSlider();
    }
    
    // Предыдущий слайд
    function prevSlide() {
        currentSlide = (currentSlide - 1 + slideCount) % slideCount;
        updateSlider();
    }
    
    // Обработчики событий
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Навигация по точкам
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateSlider();
        });
    });
    
    // Запуск слайдера
    initSlider();
});