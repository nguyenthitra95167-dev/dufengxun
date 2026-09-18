# Dufengxun.com — Privacy-First Local Tools Studio

A complete, production-ready, commercial-grade marketing website for **Dufengxun** — an independent product studio building privacy-first, design-led mobile utilities for iOS and Android.

## Project Overview

- **Team name:** dufengxun.com
- **Business support:** support@dufengxun.com
- **Contact:** contact@dufengxun.com
- **Address:** Hoa Lac Hi-Tech Park, Hanoi, Vietnam
- **Language:** English (all copy)
- **Style:** Apple-inspired minimalism with cool color palette (deep blue, cyan, indigo)
- **Animations:** Rich, with parallax, reveal-on-scroll, animated counters, hover transforms

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home — hero, what we build, products showcase, philosophy |
| `services.html` | Business services — product track + consulting track |
| `culture.html` | Team culture, principles, workflow |
| `updates.html` | News & release timeline |
| `contact.html` | Contact form & studio info |
| `privacy.html` | Privacy Policy + User Service Agreement (combined, full global-compliance edition) |
| `terms.html` | User Service Agreement (standalone) |

## Tech Stack

- **HTML5** semantic markup
- **CSS3** with custom properties, Grid, Flexbox, `backdrop-filter`, animations
- **Vanilla JavaScript** (ES6+) — no framework dependencies
- **SVG** for all icons, logo, and visual elements
- **No build step required** — open `index.html` directly

## Directory Structure

```
dufengxun/
├── index.html              Home
├── services.html           Services
├── culture.html            Culture
├── updates.html            Updates
├── contact.html            Contact
├── privacy.html            Privacy Policy + Service Agreement
├── terms.html              User Service Agreement
├── robots.txt              SEO robots file
├── sitemap.xml             XML sitemap
├── app-ads.txt             Authorized AdSense sellers (empty by default)
├── manifest.json           PWA manifest
├── .htaccess               Apache config
├── css/
│   └── style.css           All styles (~1180 lines)
├── js/
│   ├── components.js       Shared navbar/footer injection
│   └── main.js             Interactions, animations, form
├── images/                 (all generated assets)
│   ├── favicon.svg         Site favicon
│   ├── logo.svg            Full logo
│   ├── og-icon.svg         Square OG icon
│   ├── og-default.png      1200x630 social card
│   ├── hero-illustration.png    Hero background visual
│   ├── team-illustration.png    Team workspace visual
│   ├── privacy-illustration.png Shield & lock visual
│   ├── services-illustration.png 6-stage process visual
│   ├── download-illustration.png App store badges visual
│   ├── pattern.png         Dot grid texture
│   ├── app-pulsetrack.png  Phone mockup
│   ├── app-decidewise.png  Phone mockup
│   ├── app-chronoflow.png  Phone mockup
│   ├── app-moodcanvas.png  Phone mockup
│   ├── app-store-badge.svg        App Store badge
│   ├── google-play-badge.svg      Google Play badge
│   ├── iso-27001-badge.svg         ISO 27001 cert
│   └── iso-27701-badge.svg         ISO 27701 cert
└── generate_images.py      Image generator script (Pillow)
```

## Key Features

### Privacy Policy (Complete)
The `privacy.html` document is the **complete, unabridged** global compliance edition of the original Chinese document. It covers:

- **Part I — Privacy Policy** (Sections 1-10)
  - General provisions, collection scope, third-party SDKs, usage purposes, storage & security, transfer & disclosure, regional adaptations (GDPR, CCPA, LGPD, PIPL, COPPA), age policy, user rights, updates, disclaimers
  - **Ad networks covered:** Google AdMob, Google Ad Manager, Meta Audience Network, Unity Ads, AppLovin MAX, Pangle, Mintegral, Chartboost, Vungle, AdColony, Tapjoy, InMobi, Smaato, Verizon Media, Start.io, Digital Turbine, Moloco, Liftoff, Apple Search Ads
  - **Ad formats:** banner, interstitial, rewarded video, native, app-open, MREC, splash
  - **Regional laws:** EU GDPR, US CCPA/CPRA, China PIPL, Brazil LGPD, Thailand ETDA, Singapore MAS

- **Part II — User Service Agreement** (Sections 11-15)
  - Service overview, user rights & obligations, our rights & obligations, IAA + IAP terms, suspension & termination, IP, dispute resolution, miscellaneous

### SEO
- Full semantic HTML5
- Per-page `<title>`, meta description, keywords, OG/Twitter tags
- `robots.txt` and `sitemap.xml`
- Canonical URLs
- Structured data (JSON-LD on `index.html`)
- Proper heading hierarchy

### Design System
- CSS custom properties for colors, spacing, radii, transitions
- Cool color palette: `#0a0e1a` background, `#5b8def` accent, `#4fc3f7` cyan, `#8b7fd8` purple
- Apple-style typography: SF Pro Display, Inter fallbacks
- Glass-morphism cards with `backdrop-filter: blur()`
- Animated gradient text, floating orbs, grid background, scan lines

### Animations
- Hero parallax orbs
- Reveal-on-scroll using IntersectionObserver
- Animated stat counters
- Smooth scroll for anchor links
- Hover transforms on cards, icons
- Navbar background transition on scroll
- Mobile menu slide-in
- Form submit feedback
- Shimmer effect, pulse animation, scroll indicator bounce

## Browser Support

- Chrome / Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari iOS 14+
- Chrome Android 90+

## Local Development

```bash
# Python 3
python -m http.server 8080

# Node
npx serve .

# Then open http://localhost:8080
```

## Deployment

1. Upload all files to your web host preserving the directory structure
2. Ensure the host supports `.txt` and `.xml` MIME types
3. Configure your domain to point to the project root
4. Submit `sitemap.xml` to Google Search Console
5. Update `app-ads.txt` with your authorized ad network seller IDs once you have them

## License

© 2026 Dufengxun Studio. All rights reserved.

The website code is provided to Dufengxun for commercial use.
