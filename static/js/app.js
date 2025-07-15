// Custom JavaScript for the movie database app

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Enhanced movie card hover effects
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Rating stars interaction
    const ratingStars = document.querySelectorAll('.rating-interactive .fa-star');
    ratingStars.forEach((star, index) => {
        star.addEventListener('click', function() {
            const rating = index + 1;
            const ratingInput = document.getElementById('rating');
            if (ratingInput) {
                ratingInput.value = rating;
            }
            
            // Update visual feedback
            ratingStars.forEach((s, i) => {
                if (i < rating) {
                    s.classList.remove('far');
                    s.classList.add('fas');
                } else {
                    s.classList.remove('fas');
                    s.classList.add('far');
                }
            });
        });
    });

    // Search form enhancements
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const query = this.value.trim();
                if (query.length > 2) {
                    // Could add autocomplete functionality here
                    console.log('Search query:', query);
                }
            });
        }
    }

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Link copied to clipboard!', 'success');
    }, function(err) {
        console.error('Could not copy text: ', err);
        showToast('Failed to copy link', 'error');
    });
}

function showToast(message, type = 'info') {
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// Social sharing functions
function shareOnTwitter(text, url) {
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    window.open(twitterUrl, '_blank', 'width=550,height=400');
}

function shareOnFacebook(url) {
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    window.open(facebookUrl, '_blank', 'width=550,height=400');
}

// Form validation enhancements
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Rating system enhancement
function initializeRatingSystem() {
    const ratingContainers = document.querySelectorAll('.rating-interactive');
    
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.fa-star');
        const hiddenInput = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', function() {
                highlightStars(stars, index + 1);
            });
            
            star.addEventListener('click', function() {
                const rating = index + 1;
                if (hiddenInput) {
                    hiddenInput.value = rating;
                }
                setRating(stars, rating);
            });
        });
        
        container.addEventListener('mouseleave', function() {
            const currentRating = hiddenInput ? parseInt(hiddenInput.value) || 0 : 0;
            setRating(stars, currentRating);
        });
    });
}

function highlightStars(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas');
        } else {
            star.classList.remove('fas');
            star.classList.add('far');
        }
    });
}

function setRating(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas');
        } else {
            star.classList.remove('fas');
            star.classList.add('far');
        }
    });
}

// Initialize rating system when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeRatingSystem);

// Enhanced movie browsing functionality
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching with smooth transitions
    const tabs = document.querySelectorAll('.nav-pills .nav-link');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Add active to clicked tab
            this.classList.add('active');
            
            // Show corresponding content
            const target = this.getAttribute('href');
            const tabPanes = document.querySelectorAll('.tab-pane');
            
            tabPanes.forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            
            const targetPane = document.querySelector(target);
            if (targetPane) {
                targetPane.classList.add('show', 'active');
            }
        });
    });
    
    // Enhanced search with debounce
    const searchInput = document.querySelector('input[name="query"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    // Add visual feedback
                    this.classList.add('is-loading');
                    
                    // Remove loading after 2 seconds
                    setTimeout(() => {
                        this.classList.remove('is-loading');
                    }, 2000);
                }, 500);
            }
        });
    }
    
    // Genre button interactions
    const genreButtons = document.querySelectorAll('.genre-buttons .btn');
    genreButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add loading state
            this.classList.add('btn-loading');
            
            // Add visual feedback
            genreButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Quick navigation enhancements
    const quickNavButtons = document.querySelectorAll('.quick-nav-section .btn');
    quickNavButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Infinite scroll for movie results
    const movieContainer = document.querySelector('.movie-results');
    if (movieContainer) {
        let loading = false;
        let page = 1;
        
        window.addEventListener('scroll', function() {
            if (loading) return;
            
            const scrollTop = window.pageYOffset;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            
            if (scrollTop + windowHeight >= documentHeight - 1000) {
                loading = true;
                page++;
                
                // Show loading indicator
                const loader = document.createElement('div');
                loader.className = 'text-center py-3';
                loader.innerHTML = '<i class="fas fa-spinner fa-spin fa-2x"></i>';
                movieContainer.appendChild(loader);
                
                // Simulate loading (in real implementation, make API call)
                setTimeout(() => {
                    loader.remove();
                    loading = false;
                }, 2000);
            }
        });
    }
    
    // Enhanced movie card hover effects
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(card => {
        let hoverTimeout;
        
        card.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.2)';
            
            // Add subtle glow effect
            this.style.filter = 'brightness(1.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                this.style.filter = 'brightness(1)';
            }, 100);
        });
    });
});

// Advanced rating system with animations
function enhancedRatingSystem() {
    const ratingContainers = document.querySelectorAll('.rating-interactive');
    
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.fa-star');
        const feedback = container.querySelector('.rating-feedback');
        
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', function() {
                // Animate stars
                stars.forEach((s, i) => {
                    if (i <= index) {
                        s.style.transform = 'scale(1.2)';
                        s.style.color = '#ffc107';
                    } else {
                        s.style.transform = 'scale(1)';
                        s.style.color = '#6c757d';
                    }
                });
                
                // Show feedback
                if (feedback) {
                    const messages = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
                    feedback.textContent = messages[index];
                    feedback.style.opacity = '1';
                }
            });
            
            star.addEventListener('click', function() {
                // Add click animation
                this.style.transform = 'scale(1.5)';
                setTimeout(() => {
                    this.style.transform = 'scale(1.2)';
                }, 150);
                
                // Show success message
                showToast(`Rated ${index + 1} stars!`, 'success');
            });
        });
        
        container.addEventListener('mouseleave', function() {
            stars.forEach(s => {
                s.style.transform = 'scale(1)';
            });
            
            if (feedback) {
                feedback.style.opacity = '0';
            }
        });
    });
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', enhancedRatingSystem);

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Press 'S' to focus search
    if (e.key === 's' && !e.ctrlKey && !e.metaKey) {
        const searchInput = document.querySelector('input[name="query"]');
        if (searchInput && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
    
    // Press 'B' to go to browse
    if (e.key === 'b' && !e.ctrlKey && !e.metaKey) {
        const browseLink = document.querySelector('a[href*="browse"]');
        if (browseLink && document.activeElement.tagName !== 'INPUT') {
            e.preventDefault();
            browseLink.click();
        }
    }
    
    // Press 'D' to go to discover
    if (e.key === 'd' && !e.ctrlKey && !e.metaKey) {
        const discoverLink = document.querySelector('a[href*="discover"]');
        if (discoverLink && document.activeElement.tagName !== 'INPUT') {
            e.preventDefault();
            discoverLink.click();
        }
    }
});

// Enhanced toast notifications
function showEnhancedToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed animate__animated animate__slideInRight`;
    toast.style.cssText = `
        top: 20px; 
        right: 20px; 
        z-index: 9999; 
        min-width: 300px;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="${icons[type] || icons.info} me-2"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove
    setTimeout(() => {
        if (toast.parentNode) {
            toast.classList.add('animate__slideOutRight');
            setTimeout(() => {
                toast.remove();
            }, 500);
        }
    }, duration);
}

// Add ripple effect CSS
const rippleCSS = `
.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0);
    animation: ripple 0.6s linear;
    pointer-events: none;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}
`;

const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);
