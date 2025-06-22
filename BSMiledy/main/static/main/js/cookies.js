document.addEventListener('DOMContentLoaded', function() {
    if (!document.cookie.includes('cookies_accepted=true')) {
        const cookiesNotice = document.getElementById('cookies-notice');
        const acceptBtn = document.getElementById('accept-cookies');
   
        setTimeout(() => {
            cookiesNotice.style.display = 'block';
            setTimeout(() => {
                cookiesNotice.style.opacity = '1';
            }, 10);
        }, 1000);

        acceptBtn.addEventListener('click', function() {
            const date = new Date();
            date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
            document.cookie = `cookies_accepted=true; expires=${date.toUTCString()}; path=/`;
            
            cookiesNotice.style.opacity = '0';
            setTimeout(() => {
                cookiesNotice.style.display = 'none';
            }, 300);
        });
    }
});