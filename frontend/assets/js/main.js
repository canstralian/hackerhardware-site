/**
 * HackerHardware.net - Main JavaScript
 * Core functionality and UI interactions
 */

(function() {
    'use strict';

    // Mobile menu toggle
    const initMobileMenu = () => {
        const burger = document.querySelector('.navbar-burger');
        const menu = document.querySelector('.navbar-menu');

        if (burger && menu) {
            burger.addEventListener('click', () => {
                burger.classList.toggle('is-active');
                menu.classList.toggle('is-active');
            });
        }
    };

    // Smooth scroll for anchor links
    const initSmoothScroll = () => {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initMobileMenu();
            initSmoothScroll();
        });
    } else {
        initMobileMenu();
        initSmoothScroll();
    }

})();
