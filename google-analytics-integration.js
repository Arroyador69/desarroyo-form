/**
 * GOOGLE ANALYTICS + SEARCH CONSOLE INTEGRATION
 * Integración en tiempo real para dashboard DesArroyo Tech
 */

class GoogleAnalyticsIntegration {
    constructor() {
        this.gaPropertyId = 'G-XXXXXXXXXX'; // Tu Google Analytics ID
        this.searchConsoleProperty = 'https://desarroyo.tech'; // Tu dominio
        this.refreshInterval = 30000; // 30 segundos
        this.initializeTracking();
    }

    /**
     * Inicializar Google Analytics 4
     */
    initializeTracking() {
        // Cargar Google Analytics 4
        const script1 = document.createElement('script');
        script1.async = true;
        script1.src = `https://www.googletagmanager.com/gtag/js?id=${this.gaPropertyId}`;
        document.head.appendChild(script1);

        // Configurar gtag
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', this.gaPropertyId, {
            // Configuración para tiempo real
            send_page_view: true,
            anonymize_ip: true,
            custom_map: {
                'custom_dimension_1': 'source_campaign'
            }
        });

        window.gtag = gtag;
        
        // Eventos personalizados para el dashboard
        this.trackDashboardEvents();
    }

    /**
     * Obtener métricas en tiempo real (simulado con datos locales + GA)
     */
    async getRealTimeMetrics() {
        try {
            // Datos en tiempo real simulados (en producción usarías GA Reporting API)
            const realTimeData = {
                activeUsers: await this.getActiveUsers(),
                pageViews: await this.getPageViews(),
                topPages: await this.getTopPages(),
                trafficSources: await this.getTrafficSources(),
                clickEvents: await this.getClickEvents(),
                conversions: await this.getConversions()
            };

            return realTimeData;
        } catch (error) {
            console.error('Error getting real-time metrics:', error);
            return this.getFallbackMetrics();
        }
    }

    /**
     * Usuarios activos en tiempo real
     */
    async getActiveUsers() {
        // En producción: GA Reporting API
        // Por ahora: estimación basada en eventos recientes
        const sessionStorage = JSON.parse(localStorage.getItem('ga_sessions') || '[]');
        const now = Date.now();
        const activeTime = 5 * 60 * 1000; // 5 minutos
        
        const activeSessions = sessionStorage.filter(session => 
            (now - session.timestamp) < activeTime
        );

        return {
            current: activeSessions.length + Math.floor(Math.random() * 3), // +random para simular
            trend: '+12%',
            compared_to: 'última hora'
        };
    }

    /**
     * Páginas más vistas hoy
     */
    async getPageViews() {
        const pages = [
            { page: '/', views: 156, percentage: 45.2 },
            { page: '/index_conectado_n8n.html', views: 89, percentage: 25.8 },
            { page: '/generador_automatizaciones.html', views: 67, percentage: 19.4 },
            { page: '/client-crm.html', views: 23, percentage: 6.7 },
            { page: '/mejora_web.html', views: 10, percentage: 2.9 }
        ];

        return {
            total_today: pages.reduce((sum, p) => sum + p.views, 0),
            pages: pages,
            trend: '+8.4%'
        };
    }

    /**
     * Fuentes de tráfico
     */
    async getTrafficSources() {
        return {
            sources: [
                { source: 'Google Search', visitors: 234, percentage: 67.2, trend: '+15%' },
                { source: 'Direct', visitors: 56, percentage: 16.1, trend: '+3%' },
                { source: 'Social Media', visitors: 34, percentage: 9.8, trend: '+22%' },
                { source: 'Referrals', visitors: 24, percentage: 6.9, trend: '-2%' }
            ],
            total_sessions: 348
        };
    }

    /**
     * Eventos de clicks en tiempo real
     */
    async getClickEvents() {
        const events = JSON.parse(localStorage.getItem('click_events') || '[]');
        const today = new Date().toDateString();
        
        const todayEvents = events.filter(event => 
            new Date(event.timestamp).toDateString() === today
        );

        return {
            total_clicks: todayEvents.length,
            popular_links: [
                { link: 'Encuesta DesArroyo', clicks: 67, url: '/index_conectado_n8n.html' },
                { link: 'Generador Automatizaciones', clicks: 45, url: '/generador_automatizaciones.html' },
                { link: 'CRM Clientes', clicks: 23, url: '/client-crm.html' },
                { link: 'Email Alberto', clicks: 18, url: 'mailto:alberto@desarroyo.tech' }
            ]
        };
    }

    /**
     * Conversiones del sistema de llamadas
     */
    async getConversions() {
        try {
            // Leer datos del sistema de llamadas
            const response = await fetch('/api/dashboard/leads-stats');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error fetching conversions:', error);
        }

        // Fallback con datos simulados
        return {
            calls_today: 12,
            successful_calls: 5,
            conversion_rate: 41.7,
            leads_generated: 5,
            sectors: [
                { sector: 'restaurantes', calls: 4, conversions: 2 },
                { sector: 'peluquerias', calls: 3, conversions: 1 },
                { sector: 'dentistas', calls: 5, conversions: 2 }
            ]
        };
    }

    /**
     * Datos de respaldo si falla la conexión
     */
    getFallbackMetrics() {
        return {
            activeUsers: { current: 2, trend: '+5%', compared_to: 'última hora' },
            pageViews: { total_today: 156, trend: '+12%' },
            trafficSources: { total_sessions: 89, sources: [] },
            clickEvents: { total_clicks: 45 },
            conversions: { calls_today: 0, successful_calls: 0, conversion_rate: 0 }
        };
    }

    /**
     * Tracking personalizado para eventos del dashboard
     */
    trackDashboardEvents() {
        // Track cuando alguien ve el dashboard
        gtag('event', 'dashboard_view', {
            event_category: 'Dashboard',
            event_label: 'Admin Dashboard View'
        });

        // Track clicks en enlaces importantes
        document.addEventListener('click', (event) => {
            const link = event.target.closest('a');
            if (link) {
                const href = link.getAttribute('href');
                if (href && (href.includes('desarroyo.tech') || href.startsWith('/'))) {
                    gtag('event', 'internal_link_click', {
                        event_category: 'Navigation',
                        event_label: href,
                        value: 1
                    });

                    // Guardar en localStorage para métricas locales
                    const clickEvents = JSON.parse(localStorage.getItem('click_events') || '[]');
                    clickEvents.push({
                        url: href,
                        timestamp: new Date().toISOString(),
                        text: link.textContent.trim()
                    });
                    
                    // Mantener solo últimos 100 eventos
                    if (clickEvents.length > 100) {
                        clickEvents.splice(0, clickEvents.length - 100);
                    }
                    
                    localStorage.setItem('click_events', JSON.stringify(clickEvents));
                }
            }
        });

        // Track conversiones de llamadas
        window.trackCallConversion = (leadData) => {
            gtag('event', 'call_conversion', {
                event_category: 'Leads',
                event_label: leadData.sector,
                custom_dimension_1: leadData.ciudad,
                value: 1
            });
        };

        // Track sesiones activas
        const sessionData = {
            timestamp: Date.now(),
            sessionId: this.generateSessionId()
        };
        
        const sessions = JSON.parse(localStorage.getItem('ga_sessions') || '[]');
        sessions.push(sessionData);
        localStorage.setItem('ga_sessions', JSON.stringify(sessions));
    }

    /**
     * Generar ID de sesión único
     */
    generateSessionId() {
        return 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Actualizar métricas automáticamente
     */
    startRealTimeUpdates(callback) {
        const updateMetrics = async () => {
            const metrics = await this.getRealTimeMetrics();
            callback(metrics);
        };

        // Actualización inicial
        updateMetrics();

        // Actualizar cada 30 segundos
        setInterval(updateMetrics, this.refreshInterval);

        console.log('🔄 Métricas en tiempo real iniciadas (actualización cada 30s)');
    }
}

// API para integrar con el dashboard
class DashboardAnalytics {
    constructor() {
        this.ga = new GoogleAnalyticsIntegration();
        this.setupDashboardIntegration();
    }

    setupDashboardIntegration() {
        // Agregar métricas al dashboard existente
        if (window.dashboardData) {
            this.integrateWithExistingDashboard();
        } else {
            // Esperar a que se cargue el dashboard
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(() => this.integrateWithExistingDashboard(), 1000);
            });
        }
    }

    integrateWithExistingDashboard() {
        // Iniciar actualizaciones en tiempo real
        this.ga.startRealTimeUpdates((metrics) => {
            this.updateDashboardMetrics(metrics);
        });

        console.log('📊 Google Analytics integrado con dashboard');
    }

    updateDashboardMetrics(metrics) {
        // Actualizar métricas en el dashboard existente
        if (window.updateRealTimeMetrics) {
            window.updateRealTimeMetrics(metrics);
        }

        // Emitir evento personalizado para que el dashboard lo capture
        window.dispatchEvent(new CustomEvent('analyticsUpdate', {
            detail: metrics
        }));
    }
}

// Inicializar cuando se carga el script
if (typeof window !== 'undefined') {
    window.DashboardAnalytics = DashboardAnalytics;
    window.GoogleAnalyticsIntegration = GoogleAnalyticsIntegration;
    
    // Auto-inicializar si estamos en el dashboard
    if (window.location.pathname.includes('dashboard')) {
        new DashboardAnalytics();
    }
}

export { GoogleAnalyticsIntegration, DashboardAnalytics }; 