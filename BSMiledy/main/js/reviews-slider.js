document.addEventListener('DOMContentLoaded', function() {
    const sliderWrapper = document.querySelector('.reviews-slider__wrapper');
    const slides = document.querySelectorAll('.reviews-slider__slide');
    const dots = document.querySelectorAll('.reviews-slider__dot');
    const prevBtn = document.querySelector('.reviews-slider__nav-btn.prev');
    const nextBtn = document.querySelector('.reviews-slider__nav-btn.next');
    
    let currentIndex = 0;
    const slidesToShow = getSlidesToShow();
    const totalSlides = slides.length;
    
    function getSlidesToShow() {
        if (window.innerWidth >= 992) return 3;
        if (window.innerWidth >= 768) return 2;
        return 1;
    }
    
    function updateSlider() {
        const slideWidth = 100 / slidesToShow;
        const translateValue = -currentIndex * slideWidth;
        sliderWrapper.style.transform = `translateX(${translateValue}%)`;
        
        // Обновляем активные точки
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === Math.floor(currentIndex / slidesToShow));
        });
    }
    
    function nextSlide() {
        if (currentIndex < totalSlides - slidesToShow) {
            currentIndex++;
            updateSlider();
        }
    }
    
    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlider();
        }
    }
    
    function handleResize() {
        const newSlidesToShow = getSlidesToShow();
        if (newSlidesToShow !== slidesToShow) {
            currentIndex = 0;
            updateSlider();
        }
    }
    
    // Обработчики событий
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentIndex = index * slidesToShow;
            updateSlider();
        });
    });
    
    window.addEventListener('resize', handleResize);
    
    // Автопереключение
    let slideInterval = setInterval(() => {
        if (currentIndex >= totalSlides - slidesToShow) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        updateSlider();
    }, 5000);
    
    sliderWrapper.addEventListener('mouseenter', () => clearInterval(slideInterval));
    sliderWrapper.addEventListener('mouseleave', () => {
        slideInterval = setInterval(() => {
            if (currentIndex >= totalSlides - slidesToShow) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }
            updateSlider();
        }, 5000);
    });
    
    // Инициализация
    updateSlider();
});