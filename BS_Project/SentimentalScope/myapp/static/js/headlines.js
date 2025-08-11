document.addEventListener("DOMContentLoaded", function () {
  // Get CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  // Handle analyze button clicks
  const analyzeButtons = document.querySelectorAll(".analyze-btn");

  analyzeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const documentId = this.dataset.id;
      const btnText = this.querySelector(".btn-text");
      const loadingText = this.querySelector(".loading-text");

      // Disable button and show loading
      this.disabled = true;
      btnText.style.display = "none";
      loadingText.style.display = "inline-flex";

      // Send request to analyze content
      fetch("/analyze-content/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          document_id: documentId,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Show success message
            showMessage("success", data.message);

            // Redirect to analyzer
            setTimeout(() => {
              window.location.href = data.redirect_url;
            }, 1000);
          } else {
            // Show error message
            showMessage("error", data.message);

            // Re-enable button
            this.disabled = false;
            btnText.style.display = "inline";
            loadingText.style.display = "none";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showMessage(
            "error",
            "An error occurred while processing the request."
          );

          // Re-enable button
          this.disabled = false;
          btnText.style.display = "inline";
          loadingText.style.display = "none";
        });
    });
  });

  // Handle clear all button
  const clearAllBtn = document.getElementById("clear-all");
  if (clearAllBtn) {
    clearAllBtn.addEventListener("click", function () {
      if (
        confirm(
          "Are you sure you want to clear all headlines? This action cannot be undone."
        )
      ) {
        // Add loading state
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Clearing...';
        this.disabled = true;

        // Send request to clear headlines
        fetch("/clear-headlines/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              showMessage("success", data.message);
              // Reload page to show empty state
              setTimeout(() => {
                location.reload();
              }, 1000);
            } else {
              showMessage("error", data.message);
              this.innerHTML = originalText;
              this.disabled = false;
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            showMessage("error", "An error occurred while clearing headlines.");
            this.innerHTML = originalText;
            this.disabled = false;
          });
      }
    });
  }

  // Show message function
  function showMessage(type, message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll(".message");
    existingMessages.forEach((msg) => msg.remove());

    // Create new message element
    const messageDiv = document.createElement("div");
    messageDiv.className = `message message-${type}`;
    messageDiv.innerHTML = `
            <i class="fas fa-${
              type === "success" ? "check-circle" : "exclamation-circle"
            }"></i>
            ${message}
        `;

    // Insert message at the top of container
    const container = document.querySelector(".container");
    const headerSection = container.querySelector(".header-section");
    container.insertBefore(messageDiv, headerSection.nextSibling);

    // Auto remove message after 5 seconds
    setTimeout(() => {
      messageDiv.style.opacity = "0";
      setTimeout(() => {
        if (messageDiv.parentNode) {
          messageDiv.remove();
        }
      }, 300);
    }, 5000);
  }

  // Add hover effects to cards
  const headlineCards = document.querySelectorAll(".headline-card");
  headlineCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-4px)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // Add smooth scrolling for back to top
  function smoothScroll() {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe headline cards for animation
  headlineCards.forEach((card) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(card);
  });
});
