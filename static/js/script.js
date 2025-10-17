/*
==========================================
   BLOG WRITING PLATFORM - COMPLETE JS
   Modern, Interactive, Error-Free Code
==========================================
*/

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApplication();
});

function initializeApplication() {
    initNavigation();
    initForms();
    initLikeButtons();
    initSearch();
    initImageUpload();
    initFlashMessages();
    initBackToTop();
    initLazyLoading();
    initWordCount();
    initAutoSave();

    console.log('✅ Blog application initialized successfully!');
}

// Navigation functionality
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');

            // Animate hamburger menu
            const spans = navToggle.querySelectorAll('span');
            spans.forEach((span, index) => {
                if (navLinks.classList.contains('active')) {
                    if (index === 0) span.style.transform = 'rotate(45deg) translate(5px, 5px)';
                    if (index === 1) span.style.opacity = '0';
                    if (index === 2) span.style.transform = 'rotate(-45deg) translate(7px, -6px)';
                } else {
                    span.style.transform = '';
                    span.style.opacity = '';
                }
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans.forEach(span => {
                    span.style.transform = '';
                    span.style.opacity = '';
                });
            }
        });

        // Close mobile menu when clicking on links
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans.forEach(span => {
                    span.style.transform = '';
                    span.style.opacity = '';
                });
            });
        });
    }
}

// Form validation and enhancement
function initForms() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        // Add loading state to submit buttons
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.textContent || submitBtn.value;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;

                // Re-enable after timeout (in case of errors)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });

        // Real-time form validation
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateInput);
            input.addEventListener('input', clearErrors);
        });
    });

    // Password strength validation
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name === 'password') {
            input.addEventListener('input', checkPasswordStrength);
        }
    });

    // Confirm password validation
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const passwordInput = document.querySelector('input[name="password"]');

    if (confirmPasswordInput && passwordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            if (this.value !== passwordInput.value) {
                showFieldError(this, 'Passwords do not match');
            } else {
                clearFieldError(this);
            }
        });
    }
}

// Individual input validation
function validateInput(e) {
    const input = e.target;
    const value = input.value.trim();

    // Clear previous errors
    clearFieldError(input);

    // Required field validation
    if (input.hasAttribute('required') && !value) {
        showFieldError(input, 'This field is required');
        return false;
    }

    // Email validation
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(input, 'Please enter a valid email address');
            return false;
        }
    }

    // Password validation
    if (input.type === 'password' && input.name === 'password' && value) {
        if (value.length < 6) {
            showFieldError(input, 'Password must be at least 6 characters long');
            return false;
        }
    }

    return true;
}

function checkPasswordStrength(e) {
    const password = e.target.value;
    let strengthIndicator = document.getElementById('password-strength');

    if (!strengthIndicator) {
        strengthIndicator = document.createElement('div');
        strengthIndicator.id = 'password-strength';
        strengthIndicator.style.cssText = 'margin-top: 0.5rem; font-size: 0.875rem; font-weight: 500;';
        e.target.parentNode.appendChild(strengthIndicator);
    }

    let strength = 0;
    let feedback = [];

    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');

    if (/[a-z]/.test(password)) strength++;
    else feedback.push('Lowercase letter');

    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('Uppercase letter');

    if (/\d/.test(password)) strength++;
    else feedback.push('Number');

    if (/[^\w\s]/.test(password)) strength++;
    else feedback.push('Special character');

    const strengthLevels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const strengthColors = ['#ef4444', '#f59e0b', '#eab308', '#22c55e', '#10b981'];

    strengthIndicator.textContent = strengthLevels[strength] || 'Very Weak';
    strengthIndicator.style.color = strengthColors[strength] || '#ef4444';

    if (feedback.length > 0) {
        strengthIndicator.textContent += ` (Missing: ${feedback.join(', ')})`;
    }
}

function showFieldError(input, message) {
    clearFieldError(input);

    input.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: var(--error-color);
        font-size: 0.875rem;
        margin-top: 0.25rem;
        font-weight: 500;
    `;

    input.parentNode.appendChild(errorDiv);
}

function clearFieldError(input) {
    input.classList.remove('error');
    const errorDiv = input.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function clearErrors(e) {
    clearFieldError(e.target);
}

// Like button functionality
function initLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();

            const blogId = this.dataset.blogId;
            if (!blogId) return;

            // Add loading state
            const originalContent = this.innerHTML;
            this.innerHTML = '<span class="loading"></span>';
            this.disabled = true;

            try {
                const response = await fetch(`/like_blog/${blogId}`, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    const likeCount = this.querySelector('.like-count');
                    if (likeCount) {
                        likeCount.textContent = data.likes;
                    }

                    // Add visual feedback
                    this.classList.add('liked');
                    this.style.transform = 'scale(1.2)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 200);

                    showNotification('Post liked!', 'success');
                } else {
                    showNotification('Please log in to like posts', 'error');
                }
            } catch (error) {
                console.error('Error liking post:', error);
                showNotification('Failed to like post', 'error');
            } finally {
                this.innerHTML = originalContent;
                this.disabled = false;
            }
        });
    });
}

// Search functionality
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');

    if (searchInput) {
        // Auto-submit search with debounce
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3) {
                    performSearch(this.value);
                }
            }, 500);
        });

        // Add search suggestions (basic implementation)
        searchInput.addEventListener('focus', function() {
            // Could implement search suggestions here
        });
    }

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            if (!query) {
                e.preventDefault();
                showNotification('Please enter a search term', 'warning');
                searchInput.focus();
            }
        });
    }
}

function performSearch(query) {
    // Redirect to search page
    window.location.href = `/search?q=${encodeURIComponent(query)}`;
}

// Image upload functionality
function initImageUpload() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;

            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                showNotification('Image size must be less than 5MB', 'error');
                this.value = '';
                return;
            }

            // Validate file type
            if (!file.type.startsWith('image/')) {
                showNotification('Please select a valid image file', 'error');
                this.value = '';
                return;
            }

            // Show preview
            let preview = document.getElementById('image-preview');
            if (!preview) {
                preview = document.createElement('div');
                preview.id = 'image-preview';
                preview.style.cssText = 'margin-top: 1rem;';
                this.parentNode.appendChild(preview);
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = `
                    <div style="position: relative; display: inline-block;">
                        <img src="${e.target.result}" alt="Preview" style="max-width: 200px; border-radius: 8px; box-shadow: var(--shadow-sm);">
                        <button type="button" onclick="removePreview()" style="position: absolute; top: -8px; right: -8px; background: var(--error-color); color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 12px;">×</button>
                    </div>
                `;
            };
            reader.readAsDataURL(file);
        });
    });
}

function removePreview() {
    const preview = document.getElementById('image-preview');
    const imageInput = document.querySelector('input[type="file"][accept*="image"]');

    if (preview) preview.innerHTML = '';
    if (imageInput) imageInput.value = '';
}

// Flash messages
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(message => {
        // Auto-hide after 5 seconds
        const hideTimeout = setTimeout(() => {
            hideMessage(message);
        }, 5000);

        // Add close button
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '×';
        closeButton.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: inherit;
            opacity: 0.7;
            transition: opacity 0.2s ease;
        `;

        closeButton.addEventListener('click', () => {
            clearTimeout(hideTimeout);
            hideMessage(message);
        });

        closeButton.addEventListener('mouseenter', () => {
            closeButton.style.opacity = '1';
        });

        closeButton.addEventListener('mouseleave', () => {
            closeButton.style.opacity = '0.7';
        });

        message.style.position = 'relative';
        message.appendChild(closeButton);
    });
}

function hideMessage(message) {
    message.style.opacity = '0';
    message.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (message.parentNode) {
            message.remove();
        }
    }, 300);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 300px;
        padding: 1rem;
        border-radius: 8px;
        animation: slideIn 0.3s ease;
        box-shadow: var(--shadow-lg);
    `;

    document.body.appendChild(notification);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        hideMessage(notification);
    }, 4000);
}

// Word count for blog content
function initWordCount() {
    const contentTextarea = document.querySelector('#content');
    if (contentTextarea) {
        const wordCountDisplay = document.createElement('div');
        wordCountDisplay.className = 'word-count-display';
        wordCountDisplay.style.cssText = `
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
            text-align: right;
            font-weight: 500;
        `;

        contentTextarea.parentNode.appendChild(wordCountDisplay);

        function updateWordCount() {
            const text = contentTextarea.value.trim();
            const wordCount = text ? text.split(/\s+/).filter(word => word.length > 0).length : 0;
            const charCount = text.length;
            wordCountDisplay.textContent = `${wordCount} words, ${charCount} characters`;

            if (wordCount < 50) {
                wordCountDisplay.style.color = 'var(--error-color)';
            } else if (wordCount < 100) {
                wordCountDisplay.style.color = 'var(--warning-color)';
            } else {
                wordCountDisplay.style.color = 'var(--success-color)';
            }
        }

        contentTextarea.addEventListener('input', updateWordCount);
        updateWordCount(); // Initial count
    }
}

// Auto-save functionality for blog writing
function initAutoSave() {
    const blogForm = document.querySelector('#blog-form');
    if (!blogForm) return;

    const titleInput = blogForm.querySelector('#title');
    const contentTextarea = blogForm.querySelector('#content');

    if (titleInput && contentTextarea) {
        let saveTimeout;

        function autoSave() {
            const data = {
                title: titleInput.value,
                content: contentTextarea.value,
                timestamp: new Date().toISOString()
            };

            try {
                localStorage.setItem('blog_draft', JSON.stringify(data));
                showSaveIndicator();
            } catch (error) {
                console.warn('Unable to save draft:', error);
            }
        }

        function showSaveIndicator() {
            let indicator = document.querySelector('.save-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.className = 'save-indicator';
                indicator.style.cssText = `
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    background: var(--success-color);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    font-size: 0.875rem;
                    z-index: 1000;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    box-shadow: var(--shadow-md);
                `;
                document.body.appendChild(indicator);
            }

            indicator.textContent = 'Draft saved';
            indicator.style.opacity = '1';

            setTimeout(() => {
                indicator.style.opacity = '0';
            }, 2000);
        }

        [titleInput, contentTextarea].forEach(input => {
            input.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(autoSave, 2000);
            });
        });

        // Load draft on page load
        try {
            const savedDraft = localStorage.getItem('blog_draft');
            if (savedDraft) {
                const data = JSON.parse(savedDraft);
                if (confirm('A draft was found. Would you like to restore it?')) {
                    titleInput.value = data.title || '';
                    contentTextarea.value = data.content || '';
                }
            }
        } catch (error) {
            console.warn('Unable to load draft:', error);
        }

        // Clear draft on successful submit
        blogForm.addEventListener('submit', () => {
            try {
                localStorage.removeItem('blog_draft');
            } catch (error) {
                console.warn('Unable to clear draft:', error);
            }
        });
    }
}

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '↑';
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        transform: translateY(100px);
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: var(--shadow-lg);
    `;

    backToTopBtn.addEventListener('mouseenter', () => {
        backToTopBtn.style.background = 'var(--primary-hover)';
        backToTopBtn.style.transform = 'translateY(0) scale(1.1)';
    });

    backToTopBtn.addEventListener('mouseleave', () => {
        backToTopBtn.style.background = 'var(--primary-color)';
        backToTopBtn.style.transform = 'translateY(0) scale(1)';
    });

    document.body.appendChild(backToTopBtn);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.transform = 'translateY(0)';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.transform = 'translateY(100px)';
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Lazy loading for images
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
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
    }
}

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Share functionality
function sharePost(title, text, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: url || window.location.href,
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(url || window.location.href).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Unable to copy link', 'error');
        });
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeForm = document.activeElement.closest('form');
        if (activeForm) {
            activeForm.submit();
        }
    }

    // Escape to close modals/menus
    if (e.key === 'Escape') {
        const navLinks = document.querySelector('.nav-links.active');
        if (navLinks) {
            navLinks.classList.remove('active');
        }
    }
});

// Performance monitoring
function logPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }
}

logPerformance();

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send error reports to a logging service
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault();
});
