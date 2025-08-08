        // Features slider functionality
        let currentSlide = 0;
        const totalSlides = 3;
        
        function switchSlide(index) {
            const slides = document.querySelectorAll('.feature-slide');
            const dots = document.querySelectorAll('.nav-dot');
            
            // Remove all classes first
            slides.forEach(slide => {
                slide.classList.remove('active', 'previous');
            });
            dots.forEach(dot => dot.classList.remove('active'));
            
            // Add active class to current slide
            slides[index].classList.add('active');
            dots[index].classList.add('active');
            
            // Add previous class to the previous slide
            const prevIndex = (index - 1 + totalSlides) % totalSlides;
            slides[prevIndex].classList.add('previous');
            
            currentSlide = index;
        }

        // Auto switch slides every 5 seconds
        setInterval(() => {
            switchSlide((currentSlide + 1) % totalSlides);
        }, 5000);

        // Show forgot password form
        function showForgotPassword() {
            const signinForm = document.querySelector('.signin-form');
            const signupForm = document.querySelector('.signup-form');
            const forgotForm = document.querySelector('.forgot-password-form');
            const tabSwitcher = document.querySelector('.tab-switcher');
            const formHeader = document.querySelector('.form-header');

            signinForm.style.display = 'none';
            signupForm.style.display = 'none';
            tabSwitcher.style.display = 'none';
            forgotForm.style.display = 'block';
            forgotForm.style.opacity = '0';
            forgotForm.style.transform = 'translateY(30px)';
            forgotForm.style.filter = 'blur(10px)';

            // Trigger animation
            setTimeout(() => {
                forgotForm.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                forgotForm.style.opacity = '1';
                forgotForm.style.transform = 'translateY(0)';
                forgotForm.style.filter = 'blur(0)';
            }, 10);
        }

        // Show sign in form
        function showSignIn() {
            const forgotForm = document.querySelector('.forgot-password-form');
            const tabSwitcher = document.querySelector('.tab-switcher');
            
            forgotForm.style.opacity = '0';
            forgotForm.style.transform = 'translateY(10px) scale(0.95) rotate(-2deg)';
            
            setTimeout(() => {
                forgotForm.style.display = 'none';
                tabSwitcher.style.display = 'flex';
                switchTab('signin');
            }, 300);
        }

        // Tab switching functionality
        function switchTab(tab) {
            const signinForm = document.querySelector('.signin-form');
            const signupForm = document.querySelector('.signup-form');
            const tabBtns = document.querySelectorAll('.tab-btn');
            const formHeader = document.querySelector('.form-header');

            if (tab === 'signin') {
                const tabSwitcher = document.querySelector('.tab-switcher');
                tabSwitcher.classList.remove('signup');
                signupForm.classList.remove('active');
                setTimeout(() => {
                    signinForm.classList.remove('inactive');
                    signupForm.style.display = 'none';
                }, 300);
                tabBtns[0].classList.add('active');
                tabBtns[1].classList.remove('active');
                formHeader.querySelector('h2').textContent = 'Welcome Back';
                formHeader.querySelector('p').textContent = 'Sign in to continue to SentimentScope';
            } else {
                const tabSwitcher = document.querySelector('.tab-switcher');
                tabSwitcher.classList.add('signup');
                signinForm.classList.add('inactive');
                signupForm.style.display = 'block';
                setTimeout(() => {
                    signupForm.classList.add('active');
                }, 10);
                tabBtns[0].classList.remove('active');
                tabBtns[1].classList.add('active');
                formHeader.querySelector('h2').textContent = 'Create Account';
                formHeader.querySelector('p').textContent = 'Join SentimentScope to get started';
            }
        }

        // Password visibility toggle
        document.querySelectorAll('.password-toggle').forEach(button => {
            button.addEventListener('click', () => {
                const input = button.previousElementSibling;
                const icon = button.querySelector('i');
                
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            });
        });