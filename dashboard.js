// Dashboard functionality for analytics and visualization
class Dashboard {
    constructor() {
        this.charts = {};
        this.initializeDashboard();
    }
    
    async initializeDashboard() {
        await this.loadDashboardData();
        this.updateLastUpdatedTime();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            this.loadDashboardData();
            this.updateLastUpdatedTime();
        }, 30000);
    }
    
    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            this.createSkillDistributionChart(data.skill_distribution);
            this.createKeywordDistributionChart(data.keyword_distribution);
            this.createActivityChart(data.activity_chart);
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        }
    }
    
    createSkillDistributionChart(data) {
        const ctx = document.getElementById('skillChart');
        if (!ctx) return;
        
        // Destroy existing chart
        if (this.charts.skillChart) {
            this.charts.skillChart.destroy();
        }
        
        this.charts.skillChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',   // Success - Avanzado
                        'rgba(255, 193, 7, 0.8)',   // Warning - Intermedio  
                        'rgba(108, 117, 125, 0.8)'  // Secondary - Principiante
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(108, 117, 125, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            color: '#ffffff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        callbacks: {
                            label: function(context) {
                                const percentage = ((context.raw / data.data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                return `${context.label}: ${context.raw} users (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    createKeywordDistributionChart(data) {
        const ctx = document.getElementById('keywordChart');
        if (!ctx) return;
        
        // Destroy existing chart
        if (this.charts.keywordChart) {
            this.charts.keywordChart.destroy();
        }
        
        this.charts.keywordChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: [
                        'rgba(13, 202, 240, 0.8)',   // Info
                        'rgba(25, 135, 84, 0.8)',    // Success
                        'rgba(220, 53, 69, 0.8)',    // Danger
                        'rgba(255, 193, 7, 0.8)',    // Warning
                        'rgba(102, 16, 242, 0.8)',   // Indigo
                        'rgba(214, 51, 132, 0.8)'    // Pink
                    ],
                    borderColor: [
                        'rgba(13, 202, 240, 1)',
                        'rgba(25, 135, 84, 1)',
                        'rgba(220, 53, 69, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(102, 16, 242, 1)',
                        'rgba(214, 51, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            color: '#ffffff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        callbacks: {
                            label: function(context) {
                                const percentage = ((context.raw / data.data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    createActivityChart(data) {
        const ctx = document.getElementById('activityChart');
        if (!ctx) return;
        
        // Destroy existing chart
        if (this.charts.activityChart) {
            this.charts.activityChart.destroy();
        }
        
        this.charts.activityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Messages',
                    data: data.data,
                    borderColor: 'rgba(13, 202, 240, 1)',
                    backgroundColor: 'rgba(13, 202, 240, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(13, 202, 240, 1)',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff'
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#ffffff',
                            stepSize: 1
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }
    
    updateLastUpdatedTime() {
        const lastUpdatedElement = document.getElementById('lastUpdated');
        if (lastUpdatedElement) {
            const now = new Date();
            lastUpdatedElement.textContent = now.toLocaleTimeString();
        }
    }
    
    showError(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        errorAlert.style.cssText = 'top: 20px; right: 20px; z-index: 1050; max-width: 400px;';
        errorAlert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(errorAlert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorAlert.parentNode) {
                errorAlert.remove();
            }
        }, 5000);
    }
}

// Utility functions for dashboard
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});

// Add table enhancements
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to table rows
    const tables = document.querySelectorAll('.table-hover tbody tr');
    tables.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'scale(1.01)';
            row.style.transition = 'transform 0.2s ease';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'scale(1)';
        });
    });
    
    // Add click to copy functionality for usernames
    const usernames = document.querySelectorAll('.fw-medium');
    usernames.forEach(username => {
        username.style.cursor = 'pointer';
        username.title = 'Click to copy';
        
        username.addEventListener('click', () => {
            navigator.clipboard.writeText(username.textContent).then(() => {
                // Show brief success indicator
                const originalText = username.textContent;
                username.textContent = '✓ Copied';
                username.classList.add('text-success');
                
                setTimeout(() => {
                    username.textContent = originalText;
                    username.classList.remove('text-success');
                }, 1000);
            });
        });
    });
});

// Performance monitoring
let performanceData = {
    loadTime: 0,
    chartRenderTime: 0,
    apiResponseTime: 0
};

// Track page load time
window.addEventListener('load', () => {
    performanceData.loadTime = performance.now();
    console.log(`Dashboard loaded in ${performanceData.loadTime.toFixed(2)}ms`);
});

// Add real-time status updates
function updateSystemStatus() {
    const statusIndicators = document.querySelectorAll('.status-online, .status-offline');
    statusIndicators.forEach(indicator => {
        // Simulate connection status
        const isOnline = Math.random() > 0.1; // 90% uptime simulation
        
        if (isOnline) {
            indicator.className = 'status-online';
            indicator.innerHTML = '<i class="fas fa-circle me-1"></i>Online';
        } else {
            indicator.className = 'status-offline';
            indicator.innerHTML = '<i class="fas fa-circle me-1"></i>Offline';
        }
    });
}

// Update status every 10 seconds
setInterval(updateSystemStatus, 10000);
