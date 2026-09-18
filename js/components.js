/**
 * Dufengxun.com - Shared Components
 * Injects navigation and footer into all pages
 */

(function() {
    'use strict';

    const SVG_NAV = `
        <svg viewBox="0 0 32 32" fill="none">
            <defs>
                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#5b8def"/>
                    <stop offset="50%" stop-color="#4fc3f7"/>
                    <stop offset="100%" stop-color="#8b7fd8"/>
                </linearGradient>
            </defs>
            <path d="M16 2L4 9v14l12 7 12-7V9L16 2z" stroke="url(#logoGrad)" stroke-width="2" fill="none"/>
            <circle cx="16" cy="16" r="4" fill="url(#logoGrad)"/>
        </svg>
    `;

    const NAV_LINKS = [
        { href: 'index.html', label: 'Home' },
        { href: 'services.html', label: 'Services' },
        { href: 'culture.html', label: 'Culture' },
        { href: 'updates.html', label: 'Updates' },
        { href: 'insights.html', label: 'Insights' },
        { href: 'contact.html', label: 'Contact' }
    ];

    function getCurrentPage() {
        const path = window.location.pathname;
        const file = path.split('/').pop() || 'index.html';
        return file;
    }

    function renderNavbar() {
        const current = getCurrentPage();
        const nav = document.querySelector('[data-component="navbar"]');
        if (!nav) return;

        const links = NAV_LINKS.map(link => {
            const active = link.href === current ? ' active' : '';
            return `<li><a href="${link.href}" class="nav-link${active}">${link.label}</a></li>`;
        }).join('');

        nav.innerHTML = `
            <div class="nav-container">
                <a href="index.html" class="nav-logo">
                    ${SVG_NAV}
                    <span>Dufengxun</span>
                </a>
                <ul class="nav-menu">
                    ${links}
                    <li><a href="contact.html" class="nav-cta">Get Started</a></li>
                </ul>
                <button class="nav-toggle" aria-label="Toggle navigation">
                    <span></span><span></span><span></span>
                </button>
            </div>
        `;
    }

    function renderFooter() {
        const footer = document.querySelector('[data-component="footer"]');
        if (!footer) return;

        footer.innerHTML = `
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-brand">
                        <a href="index.html" class="nav-logo">
                            ${SVG_NAV}
                            <span>Dufengxun</span>
                        </a>
                        <p>An independent product studio building privacy-first, design-led mobile utilities for the global market. Crafted in Hanoi, shipped worldwide.</p>
                    </div>
                    <div class="footer-col">
                        <h4>Studio</h4>
                        <ul>
                            <li><a href="index.html">Home</a></li>
                            <li><a href="services.html">Services</a></li>
                            <li><a href="culture.html">Culture</a></li>
                            <li><a href="updates.html">Updates</a></li>
                            <li><a href="insights.html">Insights</a></li>
                            <li><a href="contact.html">Contact</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Expertise</h4>
                        <ul>
                            <li><a href="services.html#apps">App Development</a></li>
                            <li><a href="services.html#consulting">Product Consulting</a></li>
                            <li><a href="services.html#consulting">UX/UI Design</a></li>
                            <li><a href="services.html#consulting">Privacy Engineering</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Contact</h4>
                        <ul>
                            <li><a href="mailto:support@dufengxun.com">support@dufengxun.com</a></li>
                            <li><a href="mailto:contact@dufengxun.com">contact@dufengxun.com</a></li>
                            <li>Hoa Lac Hi-Tech Park<br>Hanoi, Vietnam</li>
                        </ul>
                    </div>
                </div>
                <div class="footer-bottom">
                    <div class="footer-copyright">© <span data-year>2025</span> Dufengxun Studio. All rights reserved.</div>
                    <div class="footer-legal">
                        <a href="privacy.html">Privacy Policy</a>
                        <a href="terms.html">Terms of Service</a>
                    </div>
                </div>
            </div>
        `;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            renderNavbar();
            renderFooter();
        });
    } else {
        renderNavbar();
        renderFooter();
    }
})();
