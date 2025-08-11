/**
 * Session Security JavaScript
 * Prevents back button issues and handles session security on client-side
 */

(function() {
    'use strict';
    
    // Prevent back button after login
    function preventBackButton() {
        // Clear browser history
        if (window.history && window.history.pushState) {
            window.history.pushState(null, null, window.location.href);
            window.addEventListener('popstate', function() {
                window.history.pushState(null, null, window.location.href);
                // Redirect to dashboard if user tries to go back
                if (window.location.pathname === '/auth/' || 
                    window.location.pathname === '/auth/login/' || 
                    window.location.pathname === '/auth/register/') {
                    window.location.href = '/auth/dashboard/';
                }
            });
        }
    }
    
    // Check if user is authenticated
    function checkAuthentication() {
        // This will be set by Django template if user is authenticated
        if (typeof window.isAuthenticated !== 'undefined' && window.isAuthenticated) {
            preventBackButton();
            
            // Prevent access to login/register pages when authenticated
            if (window.location.pathname === '/auth/login/' || 
                window.location.pathname === '/auth/register/' ||
                window.location.pathname === '/auth/') {
                window.location.href = '/auth/dashboard/';
            }
        }
    }
    
    // Add cache control meta tags
    function addCacheControlMeta() {
        const metaTags = [
            '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">',
            '<meta http-equiv="Pragma" content="no-cache">',
            '<meta http-equiv="Expires" content="0">'
        ];
        
        metaTags.forEach(tag => {
            if (!document.querySelector(`meta[http-equiv="${tag.match(/http-equiv="([^"]+)"/)[1]}"]`)) {
                document.head.insertAdjacentHTML('beforeend', tag);
            }
        });
    }
    
    // Handle form submissions
    function handleFormSubmissions() {
        document.addEventListener('submit', function(e) {
            if (e.target.matches('form')) {
                // Add timestamp to prevent form resubmission
                const timestamp = document.createElement('input');
                timestamp.type = 'hidden';
                timestamp.name = 'timestamp';
                timestamp.value = Date.now();
                e.target.appendChild(timestamp);
            }
        });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            addCacheControlMeta();
            checkAuthentication();
            handleFormSubmissions();
        });
    } else {
        addCacheControlMeta();
        checkAuthentication();
        handleFormSubmissions();
    }
    
    // Also run on page load
    window.addEventListener('load', function() {
        addCacheControlMeta();
        checkAuthentication();
    });
    
})();
