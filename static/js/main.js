/**
 * QR Code Generator - Main JavaScript File
 * Handles client-side interactions and validations
 */

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    initializeFormValidation();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize Bootstrap form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Show loading indicator
 * @param {string} message - Loading message to display
 */
function showLoading(message = 'Loading...') {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loadingIndicator';
    loadingDiv.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
    loadingDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    loadingDiv.style.zIndex = '9999';
    
    loadingDiv.innerHTML = `
        <div class="card shadow-lg" style="border-radius: 15px;">
            <div class="card-body p-4 text-center">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="text-muted">${message}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(loadingDiv);
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loadingDiv = document.getElementById('loadingIndicator');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

/**
 * Show success notification
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 */
function showSuccess(title, message) {
    showNotification('success', title, message);
}

/**
 * Show error notification
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 */
function showError(title, message) {
    showNotification('danger', title, message);
}

/**
 * Show warning notification
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 */
function showWarning(title, message) {
    showNotification('warning', title, message);
}

/**
 * Show info notification
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 */
function showInfo(title, message) {
    showNotification('info', title, message);
}

/**
 * Generic notification display function
 * @param {string} type - Alert type (success, danger, warning, info)
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 */
function showNotification(type, title, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '80px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.boxShadow = '0 5px 20px rgba(0,0,0,0.15)';
    alertDiv.style.borderRadius = '12px';
    
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'danger') icon = 'exclamation-triangle';
    if (type === 'warning') icon = 'exclamation-circle';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <strong>${title}</strong>
        <small>${message}</small>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Convert color hex to RGB
 * @param {string} hex - Hex color code
 * @returns {object} RGB object with r, g, b properties
 */
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

/**
 * Convert RGB to hex
 * @param {number} r - Red value
 * @param {number} g - Green value
 * @param {number} b - Blue value
 * @returns {string} Hex color code
 */
function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase();
}

/**
 * Validate email address
 * @param {string} email - Email address to validate
 * @returns {boolean} True if valid email
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate URL
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid URL
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Validate phone number (basic)
 * @param {string} phone - Phone number to validate
 * @returns {boolean} True if valid phone
 */
function isValidPhone(phone) {
    const digits = phone.replace(/\D/g, '');
    return digits.length >= 7 && digits.length <= 15;
}

/**
 * Format date to readable format
 * @param {Date} date - Date object
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    
    return date.toLocaleDateString('en-US', options);
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} length - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 50) {
    if (text.length > length) {
        return text.substring(0, length) + '...';
    }
    return text;
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @param {string} message - Success message (optional)
 */
function copyToClipboard(text, message = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Success', message);
    }).catch(() => {
        showError('Error', 'Failed to copy to clipboard');
    });
}

/**
 * Download file from URL
 * @param {string} url - File URL
 * @param {string} filename - Filename for download
 */
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Make API request with error handling
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise} Response data
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        showError('Error', error.message);
        throw error;
    }
}

/**
 * Debounce function for performance
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function for performance
 * @param {function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {function} Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Get URL query parameters
 * @returns {object} Query parameters object
 */
function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const pairs = queryString.split('&');
    
    pairs.forEach(pair => {
        const [key, value] = pair.split('=');
        params[decodeURIComponent(key)] = decodeURIComponent(value || '');
    });
    
    return params;
}

/**
 * Check if user is on mobile device
 * @returns {boolean} True if on mobile
 */
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Log analytics event
 * @param {string} category - Event category
 * @param {string} action - Event action
 * @param {string} label - Event label (optional)
 * @param {number} value - Event value (optional)
 */
function logAnalytics(category, action, label = null, value = null) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label,
            'value': value
        });
    }
}

/**
 * Export utility functions for use in other scripts
 */
window.QRGenerator = {
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showNotification,
    hexToRgb,
    rgbToHex,
    isValidEmail,
    isValidUrl,
    isValidPhone,
    formatDate,
    truncateText,
    copyToClipboard,
    downloadFile,
    apiRequest,
    debounce,
    throttle,
    getQueryParams,
    isMobileDevice,
    logAnalytics
};
