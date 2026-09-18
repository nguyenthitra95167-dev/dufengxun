/**
 * Dufengxun.com - App-level enhancements
 * Cookie consent, scroll progress, keyboard nav, etc.
 */

(function() {
    'use strict';

    function init() {
        // ===== Custom cursor =====
        initCursor();

        // ===== Page transition =====
        initPageTransitions();

        // ===== Scroll progress bar =====
        const progressBar = document.createElement('div');
        progressBar.setAttribute('aria-hidden', 'true');
        progressBar.style.cssText = 'position:fixed;top:0;left:0;height:2px;width:0;background:linear-gradient(90deg,#5b8def,#4fc3f7,#8b7fd8);z-index:9999;transition:width 0.1s linear;box-shadow:0 0 10px rgba(91,141,239,0.5);';
        document.body.appendChild(progressBar);

        let progressTicking = false;
        function updateProgress() {
            const h = document.documentElement;
            const b = document.body;
            const st = 'scrollTop';
            const sh = 'scrollHeight';
            const percent = (h[st] || b[st]) / ((h[sh] || b[sh]) - h.clientHeight) * 100;
            progressBar.style.width = (percent || 0) + '%';
            progressTicking = false;
        }
        window.addEventListener('scroll', () => {
            if (!progressTicking) {
                requestAnimationFrame(updateProgress);
                progressTicking = true;
            }
        }, { passive: true });

        // ===== Skip link =====
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        document.body.prepend(skipLink);

        // ===== Cookie consent =====
        if (!localStorage.getItem('dfx-cookie-consent')) {
            showCookieBanner();
        }

        // ===== Reading time (legal pages) =====
        const legalContent = document.querySelector('.legal-content');
        if (legalContent) {
            const text = legalContent.textContent || '';
            const words = text.trim().split(/\s+/).length;
            const minutes = Math.max(1, Math.round(words / 200));
            const meta = document.querySelector('.legal-header .meta');
            if (meta) {
                const sep = document.createElement('span');
                sep.textContent = ' · ';
                const rt = document.createElement('span');
                rt.textContent = minutes + ' min read';
                meta.appendChild(sep);
                meta.appendChild(rt);
            }
        }

        // ===== Smooth section focus on hash nav =====
        if (window.location.hash) {
            setTimeout(() => {
                const target = document.querySelector(window.location.hash);
                if (target) {
                    const offset = 80;
                    const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                    window.scrollTo({ top, behavior: 'smooth' });
                }
            }, 100);
        }
    }

    function initCursor() {
        // Skip on touch / small screens
        if (window.matchMedia('(pointer: coarse)').matches) return;

        const dot = document.createElement('div');
        const ring = document.createElement('div');
        dot.className = 'cursor-dot';
        ring.className = 'cursor-ring';
        document.body.appendChild(dot);
        document.body.appendChild(ring);
        document.body.classList.add('has-custom-cursor');

        let mx = 0, my = 0, rx = 0, ry = 0;
        let mouseTicking = false, ringTicking = false;

        document.addEventListener('mousemove', (e) => {
            mx = e.clientX;
            my = e.clientY;
            if (!mouseTicking) {
                requestAnimationFrame(() => {
                    dot.style.transform = `translate3d(${mx - 4}px, ${my - 4}px, 0)`;
                    mouseTicking = false;
                });
                mouseTicking = true;
            }
            if (!ringTicking) {
                requestAnimationFrame(() => {
                    rx += (mx - rx) * 0.15;
                    ry += (my - ry) * 0.15;
                    ring.style.transform = `translate3d(${rx - 20}px, ${ry - 20}px, 0)`;
                    ringTicking = false;
                });
                ringTicking = true;
            }
        }, { passive: true });

        // Hover effect
        document.addEventListener('mouseover', (e) => {
            const target = e.target.closest('a, button, .card, .app-card, .feature-card');
            if (target) ring.classList.add('cursor-hover');
        });
        document.addEventListener('mouseout', (e) => {
            const target = e.target.closest('a, button, .card, .app-card, .feature-card');
            if (target) ring.classList.remove('cursor-hover');
        });

        // Hide on leave
        document.addEventListener('mouseleave', () => {
            dot.style.opacity = '0';
            ring.style.opacity = '0';
        });
        document.addEventListener('mouseenter', () => {
            dot.style.opacity = '1';
            ring.style.opacity = '1';
        });
    }

    function initPageTransitions() {
        // Add fade-in on initial load
        document.body.classList.add('page-loaded');

        // Intercept internal link clicks for smooth fade
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (!link) return;
            const href = link.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:') ||
                link.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey) {
                return;
            }
            if (href.endsWith('.html') || href === 'index.html' || href === './') {
                e.preventDefault();
                document.body.classList.add('page-leaving');
                setTimeout(() => {
                    window.location.href = href;
                }, 280);
            }
        });
    }

    function showCookieBanner() {
        const banner = document.createElement('div');
        banner.className = 'cookie-banner';
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-label', 'Cookie consent');
        banner.innerHTML = `
            <div class="cookie-banner-inner">
                <div class="cookie-banner-text">
                    <strong>We respect your privacy.</strong>
                    <span>This site uses only essential cookies and never tracks you. By continuing, you agree to our <a href="privacy.html">Privacy Policy</a>.</span>
                </div>
                <div class="cookie-banner-actions">
                    <button class="cookie-btn cookie-btn-accept" data-cookie="accept">Accept</button>
                    <button class="cookie-btn cookie-btn-essential" data-cookie="essential">Essential only</button>
                </div>
            </div>
        `;
        document.body.appendChild(banner);

        // Animate in
        requestAnimationFrame(() => banner.classList.add('visible'));

        banner.querySelectorAll('[data-cookie]').forEach(btn => {
            btn.addEventListener('click', () => {
                const choice = btn.getAttribute('data-cookie');
                localStorage.setItem('dfx-cookie-consent', choice);
                localStorage.setItem('dfx-cookie-consent-time', new Date().toISOString());
                banner.classList.remove('visible');
                setTimeout(() => banner.remove(), 400);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
