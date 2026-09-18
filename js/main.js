/**
 * Dufengxun.com - Main JavaScript
 */

(function() {
    'use strict';

    function init() {
        const navbar = document.querySelector('.navbar');
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');

        if (navbar) {
            window.addEventListener('scroll', () => {
                if (window.scrollY > 30) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            });
        }

        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navToggle.classList.toggle('active');
                navMenu.classList.toggle('active');
            });

            document.querySelectorAll('.nav-menu a').forEach(link => {
                link.addEventListener('click', () => {
                    navToggle.classList.remove('active');
                    navMenu.classList.remove('active');
                });
            });
        }
    }

    // Reveal on scroll
    const revealElements = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        revealElements.forEach(el => observer.observe(el));
    } else {
        revealElements.forEach(el => el.classList.add('visible'));
    }

    // Animated counters
    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.getAttribute('data-counter'), 10);
                    const suffix = el.getAttribute('data-suffix') || '';
                    const duration = 2000;
                    const startTime = performance.now();
                    function updateCounter(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const easeProgress = 1 - Math.pow(1 - progress, 3);
                        el.textContent = Math.floor(easeProgress * target).toLocaleString() + suffix;
                        if (progress < 1) requestAnimationFrame(updateCounter);
                        else el.textContent = target.toLocaleString() + suffix;
                    }
                    requestAnimationFrame(updateCounter);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(c => counterObserver.observe(c));
    }

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const offset = 80;
                const targetPos = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: targetPos, behavior: 'smooth' });
            }
        });
    });

    // Form
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Sending...';
            setTimeout(() => {
                submitBtn.innerHTML = 'Message Sent!';
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    contactForm.reset();
                }, 2000);
            }, 1200);
        });
    }

    // Parallax
    const orbs = document.querySelectorAll('.hero-bg-orb');
    if (orbs.length > 0) {
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const scrolled = window.scrollY;
                    orbs.forEach((orb, i) => {
                        const speed = (i + 1) * 0.05;
                        orb.style.transform = `translate3d(0, ${scrolled * speed}px, 0)`;
                    });
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    // Year
    const yearEl = document.querySelector('[data-year]');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // Service worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js').catch(() => {
                // Silent fail — SW is progressive enhancement
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();