document.addEventListener('DOMContentLoaded', function() {
    // 初始化 Materialize 组件
    M.AutoInit();
    
    // 初始化轮播
    var carousel = document.querySelectorAll('.carousel.carousel-slider');
    M.Carousel.init(carousel, {
        fullWidth: true,
        indicators: true,
        duration: 500
    });
    
    // 自动轮播
    setInterval(function() {
        var instance = M.Carousel.getInstance(carousel[0]);
        if (instance) {
            instance.next();
        }
    }, 5000);
    
    // 初始化视差效果
    var parallax = document.querySelectorAll('.parallax');
    M.Parallax.init(parallax);
    
    // 初始化侧边导航
    var sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    
    // 初始化固定按钮
    var fixedActionBtn = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(fixedActionBtn, {
        direction: 'top',
        hoverEnabled: false
    });
    
    // 回到顶部功能
    var backToTopBtn = document.querySelector('.fixed-action-btn .btn-floating');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 滚动时显示/隐藏回到顶部按钮
    var fixedBtn = document.querySelector('.fixed-action-btn');
    if (fixedBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                fixedBtn.style.opacity = '1';
                fixedBtn.style.visibility = 'visible';
            } else {
                fixedBtn.style.opacity = '0';
                fixedBtn.style.visibility = 'hidden';
            }
        });
        
        // 初始状态隐藏
        fixedBtn.style.opacity = '0';
        fixedBtn.style.visibility = 'hidden';
        fixedBtn.style.transition = 'opacity 0.3s ease, visibility 0.3s ease';
    }
    
    // 搜索功能触发
    var searchTrigger = document.querySelector('.search-trigger');
    if (searchTrigger) {
        searchTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            // 这里可以添加搜索模态框或跳转到搜索页面
            alert('搜索功能开发中...');
        });
    }
    
    // 滚动动画
    var animateOnScroll = function() {
        var elements = document.querySelectorAll('.card, .card.horizontal');
        elements.forEach(function(element) {
            var elementTop = element.getBoundingClientRect().top;
            var elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // 初始动画状态
    var cards = document.querySelectorAll('.card, .card.horizontal');
    cards.forEach(function(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // 监听滚动事件
    window.addEventListener('scroll', animateOnScroll);
    
    // 初始触发一次动画
    setTimeout(animateOnScroll, 100);
    
    // 图片懒加载
    var lazyImages = document.querySelectorAll('img[data-src]');
    var imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(function(img) {
        imageObserver.observe(img);
    });
    
    // 导航栏滚动效果
    var nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 100) {
                nav.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
                nav.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            } else {
                nav.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                nav.style.boxShadow = 'none';
            }
        });
    }
    
    // 卡片悬停效果增强
    var hoverCards = document.querySelectorAll('.card.medium, .card.horizontal');
    hoverCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.08)';
        });
    });
    
    // 轮播指示器样式
    var indicators = document.querySelectorAll('.carousel .indicators .indicator-item');
    indicators.forEach(function(indicator) {
        indicator.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
    });
    
    // 页面加载完成后的动画
    window.addEventListener('load', function() {
        document.body.style.opacity = '1';
        document.body.style.transition = 'opacity 0.5s ease';
    });
    
    // 初始页面透明度
    document.body.style.opacity = '0';
    
    console.log('深度驿站博客初始化完成');
});
