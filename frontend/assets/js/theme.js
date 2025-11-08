/**
 * Theme Toggle - Dark/Light Mode Management
 * Persists preference to localStorage
 */

(function() {
    'use strict';

    const THEME_KEY = 'hackerhardware-theme';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';

    class ThemeManager {
        constructor() {
            this.html = document.documentElement;
            this.toggle = null;
            this.init();
        }

        init() {
            // Set initial theme
            this.setTheme(this.getSavedTheme() || this.getPreferredTheme());

            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.setupToggle());
            } else {
                this.setupToggle();
            }

            // Listen for system theme changes
            this.watchSystemTheme();
        }

        setupToggle() {
            this.toggle = document.querySelector('.theme-toggle');
            if (this.toggle) {
                this.toggle.addEventListener('click', () => this.toggleTheme());
            }
        }

        getPreferredTheme() {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            return mediaQuery.matches ? THEME_DARK : THEME_LIGHT;
        }

        getSavedTheme() {
            try {
                return localStorage.getItem(THEME_KEY);
            } catch (e) {
                console.warn('localStorage not available:', e);
                return null;
            }
        }

        setTheme(theme) {
            this.html.setAttribute('data-theme', theme);
            this.saveTheme(theme);
        }

        saveTheme(theme) {
            try {
                localStorage.setItem(THEME_KEY, theme);
            } catch (e) {
                console.warn('Failed to save theme preference:', e);
            }
        }

        toggleTheme() {
            const currentTheme = this.html.getAttribute('data-theme');
            const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
            this.setTheme(newTheme);
        }

        watchSystemTheme() {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

            // Only update theme if user hasn't set a preference
            mediaQuery.addEventListener('change', (e) => {
                if (!this.getSavedTheme()) {
                    this.setTheme(e.matches ? THEME_DARK : THEME_LIGHT);
                }
            });
        }
    }

    // Initialize theme manager
    new ThemeManager();

})();
