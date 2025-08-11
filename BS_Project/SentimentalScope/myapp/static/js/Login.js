// Features slider functionality
let currentSlide = 0;
const totalSlides = 3;

function switchSlide(index) {
  const slides = document.querySelectorAll(".feature-slide");
  const dots = document.querySelectorAll(".nav-dot");

  // Remove all classes first
  slides.forEach((slide) => {
    slide.classList.remove("active", "previous");
  });
  dots.forEach((dot) => dot.classList.remove("active"));

  // Add active class to current slide
  slides[index].classList.add("active");
  dots[index].classList.add("active");

  // Add previous class to the previous slide
  const prevIndex = (index - 1 + totalSlides) % totalSlides;
  slides[prevIndex].classList.add("previous");

  currentSlide = index;
}

// Auto switch slides every 5 seconds
setInterval(() => {
  switchSlide((currentSlide + 1) % totalSlides);
}, 5000);

// Show forgot password form
function showForgotPassword() {
  const signinForm = document.querySelector(".signin-form");
  const signupForm = document.querySelector(".signup-form");
  const forgotForm = document.querySelector(".forgot-password-form");
  const tabSwitcher = document.querySelector(".tab-switcher");
  const formHeader = document.querySelector(".form-header");

  signinForm.style.display = "none";
  signupForm.style.display = "none";
  tabSwitcher.style.display = "none";
  forgotForm.style.display = "block";
  forgotForm.style.opacity = "0";
  forgotForm.style.transform = "translateY(30px)";
  forgotForm.style.filter = "blur(10px)";

  // Trigger animation
  setTimeout(() => {
    forgotForm.style.transition = "all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)";
    forgotForm.style.opacity = "1";
    forgotForm.style.transform = "translateY(0)";
    forgotForm.style.filter = "blur(0)";
  }, 10);
}

// Show sign in form
function showSignIn() {
  const forgotForm = document.querySelector(".forgot-password-form");
  const tabSwitcher = document.querySelector(".tab-switcher");

  forgotForm.style.opacity = "0";
  forgotForm.style.transform = "translateY(10px) scale(0.95) rotate(-2deg)";

  setTimeout(() => {
    forgotForm.style.display = "none";
    tabSwitcher.style.display = "flex";
    switchTab("signin");
  }, 300);
}

// Tab switching functionality
function switchTab(tab) {
  const signinForm = document.querySelector(".signin-form");
  const signupForm = document.querySelector(".signup-form");
  const tabBtns = document.querySelectorAll(".tab-btn");
  const formHeader = document.querySelector(".form-header");

  // Remove all active states first
  tabBtns.forEach((btn) => btn.classList.remove("active"));
  signinForm.classList.remove("active", "inactive");
  signupForm.classList.remove("active");

  if (tab === "signin") {
    const tabSwitcher = document.querySelector(".tab-switcher");
    tabSwitcher.classList.remove("signup");

    // Hide signup form and show signin form
    signupForm.style.display = "none";
    signinForm.style.display = "block";

    // Set active states
    tabBtns[0].classList.add("active");
    formHeader.querySelector("h2").textContent = "Welcome Back";
    formHeader.querySelector("p").textContent =
      "Sign in to continue to SentimentScope";
  } else if (tab === "signup") {
    const tabSwitcher = document.querySelector(".tab-switcher");
    tabSwitcher.classList.add("signup");

    // Hide signin form and show signup form
    signinForm.style.display = "none";
    signupForm.style.display = "block";
    signupForm.classList.add("active");

    // Set active states
    tabBtns[1].classList.add("active");
    formHeader.querySelector("h2").textContent = "Create Account";
    formHeader.querySelector("p").textContent =
      "Join SentimentScope to get started";
  }
}

// Password visibility toggle
document.querySelectorAll(".password-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const input = button.previousElementSibling;
    const icon = button.querySelector("i");

    if (input.type === "password") {
      input.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
    } else {
      input.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
    }
  });
});

// Message display functions
function showMessage(message, type = "error") {
  const messageContainer = document.getElementById("messageContainer");
  const messageContent = document.getElementById("messageContent");

  messageContent.textContent = message;
  messageContainer.className = `message-container ${type}`;
  messageContainer.style.display = "block";

  // Auto hide after 5 seconds
  setTimeout(() => {
    hideMessage();
  }, 5000);
}

function hideMessage() {
  const messageContainer = document.getElementById("messageContainer");
  messageContainer.style.display = "none";
}

// Form submission helpers
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText;
  }
}

// Sign In Form Submission
function handleSignIn(event) {
  event.preventDefault();

  const form = event.target;
  const submitBtn = form.querySelector(".submit-btn");
  const formData = new FormData(form);

  // Store original button text
  if (!submitBtn.dataset.originalText) {
    submitBtn.dataset.originalText = submitBtn.innerHTML;
  }

  setButtonLoading(submitBtn, true);
  hideMessage();

  const data = {
    email: formData.get("email"),
    password: formData.get("password"),
    remember_me: formData.get("remember_me") === "on",
  };

  fetch("/signin/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      setButtonLoading(submitBtn, false);

      if (data.success) {
        showMessage(data.message, "success");
        // Redirect after a short delay
        setTimeout(() => {
          window.location.href = data.redirect_url || "/";
        }, 1500);
      } else {
        showMessage(data.message, "error");
      }
    })
    .catch((error) => {
      setButtonLoading(submitBtn, false);
      console.error("Error:", error);
      showMessage("An error occurred. Please try again.", "error");
    });
}

// Sign Up Form Submission
function handleSignUp(event) {
  event.preventDefault();

  const form = event.target;
  const submitBtn = form.querySelector(".submit-btn");
  const formData = new FormData(form);

  // Store original button text
  if (!submitBtn.dataset.originalText) {
    submitBtn.dataset.originalText = submitBtn.innerHTML;
  }

  setButtonLoading(submitBtn, true);
  hideMessage();

  const data = {
    full_name: formData.get("full_name"),
    email: formData.get("email"),
    password: formData.get("password"),
    confirm_password: formData.get("confirm_password"),
  };

  fetch("/signup/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      setButtonLoading(submitBtn, false);

      if (data.success) {
        showMessage(data.message, "success");
        // Switch to sign in form after successful registration
        setTimeout(() => {
          switchTab("signin");
          form.reset();
        }, 2000);
      } else {
        showMessage(data.message, "error");
      }
    })
    .catch((error) => {
      setButtonLoading(submitBtn, false);
      console.error("Error:", error);
      showMessage("An error occurred. Please try again.", "error");
    });
}

// Initialize the form state on page load
document.addEventListener("DOMContentLoaded", function () {
  // Ensure signin form is shown by default
  switchTab("signin");

  // Add form submission event listeners
  const signinForm = document.getElementById("signinForm");
  const signupForm = document.getElementById("signupForm");

  if (signinForm) {
    signinForm.addEventListener("submit", handleSignIn);
  }

  if (signupForm) {
    signupForm.addEventListener("submit", handleSignUp);
  }

  // Hide message when clicking outside
  document.addEventListener("click", function (event) {
    const messageContainer = document.getElementById("messageContainer");
    if (messageContainer && !messageContainer.contains(event.target)) {
      hideMessage();
    }
  });
});
