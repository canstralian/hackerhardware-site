/**
 * Metrics Dashboard - Real-time system statistics
 * Fetches and displays live metrics from the API
 */

(function() {
    'use strict';

    const API_BASE = '/api/v1';
    const METRICS_ENDPOINT = `${API_BASE}/metrics`;
    const UPDATE_INTERVAL = 5000; // 5 seconds

    class MetricsDashboard {
        constructor() {
            this.elements = {
                nodesCount: document.getElementById('nodes-count'),
                uptime: document.getElementById('uptime'),
                requests: document.getElementById('requests')
            };
            this.updateTimer = null;
            this.init();
        }

        init() {
            if (this.hasElements()) {
                this.fetchMetrics();
                this.startAutoUpdate();
            }
        }

        hasElements() {
            return Object.values(this.elements).every(el => el !== null);
        }

        async fetchMetrics() {
            try {
                const response = await fetch(METRICS_ENDPOINT);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                this.updateDisplay(data);
            } catch (error) {
                console.warn('Failed to fetch metrics:', error);
                this.showError();
            }
        }

        updateDisplay(data) {
            if (data.nodes !== undefined) {
                this.elements.nodesCount.textContent = this.formatNumber(data.nodes);
            }

            if (data.uptime !== undefined) {
                this.elements.uptime.textContent = this.formatUptime(data.uptime);
            }

            if (data.requests_per_second !== undefined) {
                this.elements.requests.textContent = this.formatNumber(data.requests_per_second);
            }
        }

        showError() {
            Object.values(this.elements).forEach(el => {
                if (el) el.textContent = '—';
            });
        }

        formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            }
            if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        }

        formatUptime(seconds) {
            const days = Math.floor(seconds / 86400);
            const hours = Math.floor((seconds % 86400) / 3600);

            if (days > 0) {
                return `${days}d ${hours}h`;
            }
            if (hours > 0) {
                return `${hours}h`;
            }
            return `${Math.floor(seconds / 60)}m`;
        }

        startAutoUpdate() {
            this.updateTimer = setInterval(() => {
                this.fetchMetrics();
            }, UPDATE_INTERVAL);
        }

        stopAutoUpdate() {
            if (this.updateTimer) {
                clearInterval(this.updateTimer);
                this.updateTimer = null;
            }
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => new MetricsDashboard());
    } else {
        new MetricsDashboard();
    }

})();
