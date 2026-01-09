// ===== Hamburger Menu Toggle =====
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger
            this.style.gap = navMenu.classList.contains('active') ? '8px' : '6px';
        });

        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }
});

// ===== Smooth Scrolling =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== Navbar Sticky Effect =====
const navbarContainer = document.querySelector('.navbar-container');
let lastScrollTop = 0;

window.addEventListener('scroll', function() {
    if (navbarContainer) {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add shadow on scroll
        if (scrollTop > 50) {
            navbarContainer.style.boxShadow = 'var(--shadow-lg)';
        } else {
            navbarContainer.style.boxShadow = 'var(--shadow-md)';
        }
        
        lastScrollTop = scrollTop;
    }
});

// ===== Fade In Animation on Scroll =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe cards and sections
document.querySelectorAll('.card, .section-title, .hero, .topic-card, .scheme-card, .wellness-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ===== Search Functionality =====
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch(this.value);
        }
    });

    document.querySelector('.search-btn').addEventListener('click', function() {
        performSearch(searchInput.value);
    });
}

function performSearch(query) {
    if (query.trim()) {
        // You can add search functionality here
        console.log('Searching for:', query);
    }
}

// ===== Active Navigation Link =====
function setActiveNav() {
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '/' && href === '/')) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '600';
        }
    });
}

setActiveNav();

// ===== Loading Animation =====
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
});

// ===== Button Hover Effects =====
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = 'var(--shadow-lg)';
    });

    btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
    });
});

// ===== Emergency Button Handler =====
const emergencyBtn = document.querySelector('.emergency-btn');
if (emergencyBtn) {
    emergencyBtn.addEventListener('click', function(e) {
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        if (!isMobile) {
            e.preventDefault();
            navigator.clipboard.writeText('112');
            showNotification('Emergency number 112 copied to clipboard!');
        }
    });
}

// ===== Notification Toast =====
function showNotification(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--primary-color);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 2000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ===== Animations =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }

    @keyframes loading {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }
`;
document.head.appendChild(style);

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape to close mobile menu
    if (e.key === 'Escape') {
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu) {
            navMenu.classList.remove('active');
        }
    }
});

// ===== Dark Mode Toggle (Optional) =====
function toggleDarkMode() {
    document.documentElement.style.filter = document.documentElement.style.filter === 'invert(1)' ? 'none' : 'invert(1)';
}

// ===== Page Load Analytics =====
window.addEventListener('load', function() {
    console.log('HealthHub Platform loaded successfully');
});

// ===== Error Boundary =====
window.addEventListener('error', function(e) {
    console.error('An error occurred:', e.error);
});

// ===== Performance Optimization =====
if ('IntersectionObserver' in window) {
    // Lazy load images
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}
